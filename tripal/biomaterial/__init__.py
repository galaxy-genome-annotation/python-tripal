from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class BiomaterialClient(Client):
    """Manage Tripal biomaterials"""

    def add_biomaterial(self, organism_id, file_path, file_type, no_wait=False):
        """
        Add a new biomaterial to the database

        :type organism_id: str
        :param organism_id: The id of the associated organism

        :type file_path: str
        :param file_path: The path to the biomaterial file

        :type file_type: str
        :param file_type: The type of the biomaterial file (xml, tsv or csv)

        :rtype: dict
        :return: Job information
        """

        if file_type not in ['xml', 'tsv', 'csv']:
            raise Exception("File format must be one of ['xml', 'tsv', 'csv']")

        if file_type == "xml":
            job_args = [file_path, organism_id]
            callback = 'xml_biomaterial_parser'

        else:
            job_args = [file_path, organism_id, file_type]
            callback = 'flat_biomaterial_parser'

        r = self.tripal.job.add_job("Add Biomaterial", 'tripal_analysis_expression', callback, job_args)

        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])
