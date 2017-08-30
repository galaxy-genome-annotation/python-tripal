from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import json
import logging
import time
from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class JobClient(Client):
    CLIENT_BASE = '/tripal_api/'

    def get_jobs(self, job_id=None):
        """
        Get all jobs

        :type job_id: int
        :param job_id: job id

        :rtype: list of dict
        :return: Jobs information
        """

        if job_id:
            return [self._get('job/%s' % job_id, {})]
        else:
            return self._get('job', {})

    def add_job(self, name, module, callback, arguments, priority=10):
        """
        Schedule a new job

        :type name: str
        :param name: The name of the job

        :type module: str
        :param module: The Tripal module name to invoke

        :type callback: str
        :param callback: The Tripal module callback function to invoke

        :type arguments: str
        :param arguments: A JSON string representing an array of arguments (e.g. "['some', 'arg', 42, 'foo']")

        :type priority: int
        :param priority: An integer score to prioritize the job

        :rtype: dict
        :return: Job information
        """

        # Ensure we will send an array whatever the input is
        if not isinstance(arguments, list) and not isinstance(arguments, dict):
            arguments = json.loads(arguments)

        data = {
            'name': name,
            'modulename': module,
            'callback': callback,
            'arguments': arguments,
            'priority': priority,
        }

        return self._request('job', data)

    def run_jobs(self, wait=True):
        """
        Run jobs in queue. There is no way to trigger a single job execution.

        :type wait: bool
        :param wait: Wait for job completion

        :rtype: dict
        :return: Job information
        """

        res = None
        while res is None or res['status'] == 'busy':
            res = self._request('job/run', {})
            if res['status'] == 'busy':
                if not wait:
                    return res
                time.sleep(20)

        return res

    def wait(self, job_id):
        """
        Wait for a job completion

        :type job_id: int
        :param job_id: job id

        :rtype: dict
        :return: Job information
        """

        job = None
        while not job or job['status'] not in ('Completed', 'Cancelled', 'Error'):
            # First call is_running to make sure the job status is updated in case it
            # exited in a wrong way
            self._check_running()

            job = self.get_jobs(job_id)
            if not job:
                raise Exception("Could not find job %s" % job_id)
            job = job[0]
            time.sleep(20)

        return job

    def _check_running(self):

        return self._request('job/is_running', {})

    def get_logs(self, stdout, stderr):
        """
        Get job output

        :type stdout: str
        :param stdout: Path to stdout file, as returned by run_jobs

        :type stderr: str
        :param stderr: Path to stderr file, as returned by run_jobs

        :rtype: dict
        :return: Output information
        """

        res = self._request('job/logs', {'stdout': stdout, 'stderr': stderr})

        res['stdout'] = json.loads(res['stdout'])
        res['stderr'] = json.loads(res['stderr'])

        return res
