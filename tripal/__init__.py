import requests
import json
import collections
import logging
from datetime import datetime
logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


def TripalAuth(parser):
    parser.add_argument('tripal', help='Complete Tripal URL')
    parser.add_argument('username', help='Admin Username')
    parser.add_argument('password', help='Admin Password')

def TripalAnalysis(parser):
    parser.add_argument("--analysis-name", required=True, help="Analysis name")
    parser.add_argument("--analysis-program", required=True, help="Program name")
    parser.add_argument("--analysis-program-version", required=True, help="Program version")
    parser.add_argument("--analysis-algorithm", help="Algorithm name")
    parser.add_argument("--analysis-source-name", required=True, help="Source name")
    parser.add_argument("--analysis-source-version", help="Source version")
    parser.add_argument("--analysis-description", help="Analysis description")
    parser.add_argument("--analysis-source-uri", help="Source URI")
    parser.add_argument("--analysis-date-executed", help="Date of execution of the analysis (format=YYYY-MM-DD, default=today)")

class TripalInstance(object):

    def __init__(self, tripal, username, password, **kwargs):
        self.tripal_url = tripal
        self.username = username
        self.password = password

        self.jobs = JobsClient(self)
        self.analysis = AnalysisClient(self)
        self.organism = OrganismClient(self)
        self.db = DbClient(self)

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


class AnalysisClient(Client):
    CLIENT_BASE = '/tripal_api/'

    def getAnalyses(self):
        return self.get('node', {})

    def getAnalysis(self, jobId):
        return self.get('node/%s' % jobId, {})

    def getAnalysisByName(self, name):
        data = {
            'table': 'analysis',
        }

        analyses = self.request('chado/list', data)

        for a in analyses:
            if a['name'] == name:
                return a

        raise Exception("Could not find the analysis %s." % (name))

    def getBasePayload(self, args):
        date = datetime.today()
        if args.analysis_date_executed:
            date = datetime.strptime(args.analysis_date_executed, '%Y-%m-%d')

        return {
                'analysisname': args.analysis_name,
                'program': args.analysis_program,
                'programversion': args.analysis_program_version,
                'algorithm': args.analysis_algorithm,
                'sourcename': args.analysis_source_name,
                'sourceversion': args.analysis_source_version,
                'sourceuri': args.analysis_source_uri,
                'description': args.analysis_description,
                'timeexecuted[day]': date.strftime('%d'),
                'timeexecuted[month]': date.strftime('%m'),
                'timeexecuted[year]': date.strftime('%Y'),
            }

    def addAnalysis(self, params):

        return self.request('node', params)

class OrganismClient(Client):
    CLIENT_BASE = '/tripal_api/'

    def getOrganisms(self):
        return self.get('node', {})

    def getOrganism(self, jobId):
        return self.get('node/%s' % jobId, {})

    def getOrganismByName(self, name):
        data = {
            'table': 'organism',
        }

        orgs = self.request('chado/list', data)

        for o in orgs:
            if o['common_name'] == name or o['abbreviation'] == name:
                return o

        raise Exception("Could not find the organism %s." % (name))

    def addOrganism(self, params):

        return self.request('node', params)

class DbClient(Client):
    CLIENT_BASE = '/tripal_api/'

    def getDbByName(self, name):
        data = {
            'table': 'db',
        }

        orgs = self.request('chado/list', data)

        for o in orgs:
            if o['name'] == name:
                return o

        raise Exception("Could not find the Db %s." % (name))
