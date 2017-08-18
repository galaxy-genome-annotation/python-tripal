"""Base tripal client
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import click
import json
import requests

from future import standard_library
standard_library.install_aliases()


class Client(object):
    """
    Base client class implementing methods to make queries to the server
    """

    def __init__(self, tripalinstance, **requestArgs):
        self.tripal = tripalinstance

        self.__verify = requestArgs.get('verify', True)
        self._requestArgs = requestArgs
        self._session = None

        if 'verify' in self._requestArgs:
            del self._requestArgs['verify']

    def _get_csrf_token(self):

        url = self.tripal.tripal_url + self.CLIENT_BASE

        headers = {
            'Content-Type': 'application/json'
        }

        if self._session:
            headers['Cookie'] = self._session

        auth = None
        if self.tripal.auth_login and self.tripal.auth_password:
            auth = (self.tripal.auth_login, self.tripal.auth_password)

        # First get a CSRF token
        r = requests.post(url + 'user/token.json', headers=headers,
                          verify=self.__verify, auth=auth, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            return d['token']
        else:
            # @see self.body for HTTP response body
            raise Exception("Unexpected response from tripal while getting CSRF token %s: %s" %
                            (r.status_code, r.text))

    def _login(self):

        # First get a CSRF token
        csrfToken = self._get_csrf_token()

        # Then login
        url = self.tripal.tripal_url + self.CLIENT_BASE

        headers = {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken
        }

        data = {
            'username': self.tripal.username,
            'password': self.tripal.password,
        }

        auth = None
        if self.tripal.auth_login and self.tripal.auth_password:
            auth = (self.tripal.auth_login, self.tripal.auth_password)

        r = requests.post(url + 'user/login.json', data=json.dumps(data), headers=headers,
                          verify=self.__verify, auth=auth, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            self._session = d['session_name'] + '=' + d['sessid']
        else:
            # @see self.body for HTTP response body
            raise Exception("Unexpected response from tripal while logging in %s: %s" %
                            (r.status_code, r.text))

    def _request(self, clientMethod, data, post_params={}):
        url = self.tripal.tripal_url + self.CLIENT_BASE + clientMethod

        if not self._session:
            self._login()

        # Get a CSRF token
        csrfToken = self._get_csrf_token()

        headers = {
            'Content-Type': 'application/json',
            'Cookie': self._session,
            'X-CSRF-Token': csrfToken
        }

        auth = None
        if self.tripal.auth_login and self.tripal.auth_password:
            auth = (self.tripal.auth_login, self.tripal.auth_password)

        r = requests.post(url, data=json.dumps(data), headers=headers,
                          verify=self.__verify, auth=auth, params=post_params, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            return d

        # @see self.body for HTTP response body
        raise Exception("Unexpected response from tripal %s: %s" %
                        (r.status_code, r.text))

    def _get(self, clientMethod, get_params):
        url = self.tripal.tripal_url + self.CLIENT_BASE + clientMethod

        if not self._session:
            self._login()

        headers = {
            'Content-Type': 'application/json',
            'Cookie': self._session  # "SESSc9c711a015d1f2624abf5bff20b25337=FQ4HGEDbfXVEeU9YTGEQMTHyE-VsspsdaNVxhFsVN0k"
        }

        auth = None
        if self.tripal.auth_login and self.tripal.auth_password:
            auth = (self.tripal.auth_login, self.tripal.auth_password)

        r = requests.get(url, headers=headers, verify=self.__verify,
                         params=get_params, auth=auth, **self._requestArgs)

        if r.status_code == 200:
            d = r.json()
            return d

        # @see self.body for HTTP response body
        raise Exception("Unexpected response from tripal %s: %s" %
                        (r.status_code, r.text))

    def _run_job_and_wait(self, job_id):
        run_res = self.tripal.job.run_jobs()
        self.tripal.job.wait(job_id)

        logs = self.tripal.job.get_logs(run_res['stdout'], run_res['stderr'])

        if logs['status'] == 'ok':
            print(logs['stdout'])
            click.echo(click.style(logs['stderr'], bold=True, fg='red'), err=True)
            return ''
        else:
            return logs
