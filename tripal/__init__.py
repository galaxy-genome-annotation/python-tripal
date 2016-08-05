import requests
import json
import collections
import logging
logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


def TripalAuth(parser):
    parser.add_argument('tripal', help='Complete Tripal URL')
    parser.add_argument('username', help='Admin Username')
    parser.add_argument('password', help='Admin Password')

class TripalInstance(object):

    def __init__(self, url, username, password):
        self.tripal_url = url
        self.username = username
        self.password = password

        self.jobs = JobsClient(self)

    def __str__(self):
        return '<TripalInstance at %s>' % self.tripal_url

class Client(object):

    def __init__(self, tripalinstance, **requestArgs):
        self._tripal = tripalinstance

        self.__verify = requestArgs.get('verify', True)
        self._requestArgs = requestArgs
        self._session = None

        if 'verify' in self._requestArgs:
            del self._requestArgs['verify']

    def getCsrfToken(self):

        url = self._tripal.tripal_url + self.CLIENT_BASE

        headers = {
            'Content-Type': 'application/json'
        }

        if self._session:
            headers['Cookie'] = self._session

        # First get a CSRF token
        r = requests.post(url + 'user/token.json', headers=headers,
                          verify=self.__verify, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            return d['token']
        else:
            # @see self.body for HTTP response body
            raise Exception("Unexpected response from tripal while getting CSRF token %s: %s" %
                            (r.status_code, r.text))

    def login(self):

        # First get a CSRF token
        csrfToken = self.getCsrfToken()

        # Then login
        url = self._tripal.tripal_url + self.CLIENT_BASE

        headers = {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken
        }

        data = {
            'username': self._tripal.username,
            'password': self._tripal.password,
        }

        r = requests.post(url + 'user/login.json', data=json.dumps(data), headers=headers,
                          verify=self.__verify, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            self._session = d['session_name'] + '=' + d['sessid']
        else:
            # @see self.body for HTTP response body
            raise Exception("Unexpected response from tripal while logging in %s: %s" %
                            (r.status_code, r.text))

    def request(self, clientMethod, data, post_params={}):
        url = self._tripal.tripal_url + self.CLIENT_BASE + clientMethod

        if not self._session:
            self.login()

        # Get a CSRF token
        csrfToken = self.getCsrfToken()

        headers = {
            'Content-Type': 'application/json',
            'Cookie': self._session,
            'X-CSRF-Token': csrfToken
        }

        r = requests.post(url, data=json.dumps(data), headers=headers,
                          verify=self.__verify, params=post_params, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            return d

        # @see self.body for HTTP response body
        raise Exception("Unexpected response from tripal %s: %s" %
                        (r.status_code, r.text))

    def get(self, clientMethod, get_params):
        url = self._tripal.tripal_url + self.CLIENT_BASE + clientMethod

        if not self._session:
            self.login()

        headers = {
            'Content-Type': 'application/json',
            'Cookie': self._session # "SESSc9c711a015d1f2624abf5bff20b25337=FQ4HGEDbfXVEeU9YTGEQMTHyE-VsspsdaNVxhFsVN0k"
        }

        r = requests.get(url, headers=headers, verify=self.__verify,
                         params=get_params, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            return d

        # @see self.body for HTTP response body
        raise Exception("Unexpected response from tripal %s: %s" %
                        (r.status_code, r.text))


class JobsClient(Client):
    CLIENT_BASE = '/tripal_api/'

    def getJobs(self):
        return self.get('job', {})

    def getJob(self, jobId):
        return self.get('job/%s' % jobId, {})

    def addJob(self, job_name, modulename, callback, arguments, priority=10):
        data = {
            'name': job_name,
            'modulename': modulename,
            'callback': callback,
            'arguments': arguments,
            'priority': priority,
        }

        return self.request('job', data)
