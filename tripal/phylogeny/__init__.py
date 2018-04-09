from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from collections import OrderedDict
from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class PhylogenyClient(Client):
    """Manage Tripal phylogeny"""

    def sync(self, max_sync='', job_name=None, no_wait=None):
        """
        Synchronize some phylotree

        :type max_sync: str
        :param max_sync: Maximum number of features to sync (default: all)

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """

        if not job_name:
            job_name = 'Sync Phylotrees'

        job_args = OrderedDict()
        job_args['base_table'] = 'phylotree'
        job_args['max_sync'] = max_sync
        job_args['organism_id'] = ''
        job_args['types'] = []
        job_args['ids'] = []
        job_args['linking_table'] = 'chado_phylotree'
        job_args['node_type'] = 'chado_phylotree'

        r = self.tripal.job.add_job(job_name, 'chado_phylotree', 'chado_node_sync_records', job_args)
        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])
