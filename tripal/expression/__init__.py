from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class ExpressionClient(Client):
    """Manage Tripal expressions"""

    def add_expression(self, organism, analysis, feature_match, file_type, file_path,
                      biomaterial_provider=None, array_design=None, assay_id=None,
                      acquisition_id=None, quantification_id=None, file_extension=None,
                      start_regex=None, stop_regex=None, no_wait=False):
        """
        :type organism: str
        :param organism: Organism Id

        :type analysis: str
        :param analysis: Id of the analysis

        :type feature_match: str
        :param organism: Match to features using either name or unique_name

        :type file_type: str
        :param file_type: Expresssion file type : column or matrix

        :type file_path: str
        :param file_path: Path to the expression file, or directory containing multiple expression files.

        :type biomaterial_provider: str
        :param biomaterial_provider: The contact who provided the biomaterial. (optional)

        :type array_design: str
        :param array_design: The array design associated with this analysis. This is not required if the experimental data was gathered from next generation sequencing methods. (optional)

        :type assay_id: str
        :param assay_id: The id of the assay associated with the experiment. (optional)

        :type acquisition_id: str
        :param acquisition_id: The id of the acquisition associated with the experiment (optional)

        :type quantification_id: str
        :param quantification_id: The id of the quantification associated with the experiment (optional)

        :type file_extension: str
        :param file_extension: File extension for the file(s) to be loaded into Chado. Do not include the ".". Not required for matrix files. (optional)

        :type start_regex: str
        :param start_regex: A regular expression to describe the line that occurs before the start of the expression data. If the file has no header, this is not needed. (optional)

        :type stop_regex: str
        :param stop_regex: A regular expression to describe the line that occurs after the end of the expression data. If the file has no footer text, this is not needed. (optional)

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :rtype: str
        :return: Loading information
        """

        if file_type == "column" and not file_extension:
            raise Exception("File_extension is required for column files")

        if file_type == "matrix":
            file_type = "mat"
        else:
            file_type = "col"

        if feature_match == "unique_name":
            feature_match = "uniq"

        job_args = [organism, analysis, biomaterial_provider, array_design, assay_id, acquisition_id, quantification_id, file_path, file_extension, file_type, start_regex, stop_regex, feature_match]

        r = self.tripal.job.add_job("Add Expression", 'tripal_analysis_expression', 'tripal_expression_loader', job_args)

        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])
