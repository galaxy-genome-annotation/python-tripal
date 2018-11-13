from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
from collections import OrderedDict

from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class ExpressionClient(Client):
    """Manage Tripal expressions"""

    def get_biomaterials_tripal(self, biomaterial_id=None):
        """
        Get Biomaterial entities

        :type biomaterial_id: int
        :param biomaterial_id: A biomaterial entity ID

        :rtype: list of dict
        :return: Organism entity information
        """

        if self.tripal.version == 3:
            if biomaterial_id:
                entities = [self._get_ws('Biological_Sample/%s' % biomaterial_id, {})]
            else:
                entities = self._get_ws('Biological_Sample', {})
        else:
            if biomaterial_id:
                entities = [self._get('node/%s' % biomaterial_id, {})]
            else:
                entities = self._get('node', {})
                entities = [n for n in entities if n['type'] == 'chado_biomaterial']

        # Return type is a dict if no biomaterial_id, list otherwise..
        # Its also a list in tripalV2.

        return entities

    def add_expression(self, organism_id, analysis_id, file_path,
                       match_type="uniquename", array_design_id=None, quantification_units=None,
                       file_extension=None, start_regex=None, stop_regex=None, seq_type=None, use_column=False, no_wait=False):
        """
        Add an expression file to tripal

        :type organism_id: str
        :param organism_id: Organism Id

        :type analysis_id: str
        :param analysis_id: Id of the analysis

        :type match_type: str
        :param match_type: Match to features using either name or uniquename. Default to uniquename

        :type file_path: str
        :param file_path: Path to the expression file, or directory containing multiple expression files

        :type array_design_id: str
        :param array_design_id: The array design ID associated with this analysis. (Non functional in Tripal2)

        :type quantification_units: str
        :param quantification_units: The units associated with the loaded values (ie, FPKM, RPKM, raw counts).

        :type file_extension: str
        :param file_extension: File extension for the file(s) to be loaded into Chado. Do not include the ".". Not required for matrix files.

        :type start_regex: str
        :param start_regex: A regular expression to describe the line that occurs before the start of the expression data. If the file has no header, this is not needed.

        :type seq_type: str
        :param seq_type: Specify the feature type to associate the data with. (Tripal3 only)

        :type stop_regex: str
        :param stop_regex: A regular expression to describe the line that occurs after the end of the expression data. If the file has no footer text, this is not needed.

        :type use_column: bool
        :param use_column: Set if the expression file is a column file

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :rtype: str
        :return: Loading information
        """

        if use_column:
            file_type = "col"
        else:
            file_type = "mat"

        if file_type == "col" and not file_extension:
            raise Exception("File_extension is required for column files")

        if match_type not in ["uniquename", "name"]:
            raise Exception("match_type should be 'name' or 'uniquename'")

        # Parameters required by the function, but not currently used...

        # These are called 'date' in V3, but they are not used anyway so...
        assay_id = None
        acquisition_id = None
        quantification_id = None
        biomaterial_provider_id = None

        if self.tripal.version == 3:

            job_args = {
                "organism_id": organism_id,
                "analysis_id": analysis_id,
                "re_start": start_regex,
                "re_stop": stop_regex,
                "fileext": file_extension,
                "filetype": file_type,
                "seqtype": seq_type,
                "feature_uniquenames": match_type,
                "arraydesign_id": array_design_id,
                "quantificationunits": quantification_units
            }

            job_name = "Importing Expression file"

            r = self.tripal.job.add_import_job(job_name, "tripal_expression_data_loader", file_path, job_args)

        elif self.tripal.version == 2:

            if match_type == "uniquename":
                match_type = "uniq"

            job_args = [organism_id, analysis_id, biomaterial_provider_id, array_design_id,
                        assay_id, acquisition_id, quantification_id, file_path, file_extension,
                        file_type, start_regex, stop_regex, match_type]

            r = self.tripal.job.add_job("Add Expression", 'tripal_analysis_expression', 'tripal_expression_loader', job_args)
        else:
            raise Exception("Tripal version not supported")

        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def get_biomaterials(self, biomaterial_name="", provider_id="", biomaterial_id="", organism_id="", dbxref_id=""):
        """
        List biomaterials in the database

        :type organism_id: str
        :param organism_id: Limit query to the selected organism

        :type biomaterial_id: str
        :param biomaterial_id: Limit query to the selected biomaterial

        :type biomaterial_name: str
        :param biomaterial_name: Limit query to the selected biomaterial

        :type provider_id: str
        :param provider_id: Limit query to the selected provider

        :type dbxref_id: str
        :param dbxref_id: Limit query to the selected ref

        :rtype: dict
        :return: Biomaterial list
        """
        orgs = self._request('chado/list', {'table': 'biomaterial'})
        if biomaterial_id:
            orgs = [v for v in orgs if v['biomaterial_id'] == str(biomaterial_id)]
        if biomaterial_name:
            orgs = [v for v in orgs if v['name'] == str(biomaterial_name)]
        if provider_id:
            orgs = [v for v in orgs if v['biosourceprovider_id'] == str(provider_id)]
        if organism_id:
            orgs = [v for v in orgs if v['taxon_id'] == str(organism_id)]
        if dbxref_id:
            orgs = [v for v in orgs if v['dbxref_id'] == str(dbxref_id)]
        return orgs

    def add_biomaterial(self, organism_id, file_path, file_type, analysis_id=None, no_wait=False):
        """
        Add a new biomaterial file to the database

        :type organism_id: str
        :param organism_id: The id of the associated organism

        :type analysis_id: str
        :param analysis_id: The id of the associated analysis. Required for TripalV3

        :type file_path: str
        :param file_path: The path to the biomaterial file

        :type file_type: str
        :param file_type: The type of the biomaterial file (xml, tsv or csv)

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :rtype: dict
        :return: Job information
        """

        if file_type not in ['xml', 'tsv', 'csv']:
            raise Exception("File format must be one of ['xml', 'tsv', 'csv']")

        if self.tripal.version == 2:

            if file_type == "xml":
                job_args = [file_path, organism_id]
                callback = 'xml_biomaterial_parser'

            else:
                job_args = [file_path, organism_id, file_type]
                callback = 'flat_biomaterial_parser'

            r = self.tripal.job.add_job("Add Biomaterial", 'tripal_analysis_expression', callback, job_args)

        elif self.tripal.version == 3:

            # TODO : Fill out insert_field and cvalue properly

            job_args = {
                "organism_id": organism_id,
                "analysis_id": analysis_id,
                "field_info": [],
                "cvalue_info": []
            }

            job_name = "Importing Biomaterial file"

            r = self.tripal.job.add_import_job(job_name, "tripal_biomaterial_loader_v3", file_path, job_args)

        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def delete_biomaterials(self, names=[], organism_id="", analysis_id="", job_name="", no_wait=False):
        """
        Delete some biomaterials

        :type names: str
        :param names: JSON list of biomaterial names to delete. (optional)

        :type organism_id: str
        :param organism_id: Organism id from which to delete biomaterials (optional)

        :type analysis_id: str
        :param analysis_id: Analysis id from which to delete biomaterials (optional)

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :type job_name: str
        :param job_name: Name of the job (optional)

        :rtype: str
        :return: status
        """

        if self.tripal.version == 3:
            raise NotImplementedError("The delete_biomaterials method is not supported in tripal V3. Please use python-chado")

        if not isinstance(names, list) and not isinstance(names, dict):
            names = json.loads(names)

        # Convert to space separated string
        names = " ".join(names)

        if(not (names or organism_id or analysis_id)):
            raise Exception("Please provide either a list of biomaterial names, an analysis id, or an organism id")

        if not job_name:
            job_name = 'Delete Biomaterials'

        job_args = OrderedDict()
        job_args['biomaterial_names'] = names
        job_args['organism_id'] = organism_id
        job_args['analysis_id'] = analysis_id

        r = self.tripal.job.add_job(job_name, 'tripal_biomaterial', 'tripal_biomaterial_delete_biomaterials', job_args)
        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def sync_biomaterials(self, ids="[]", max_sync='', job_name=None, no_wait=False):
        """
        Synchronize some biomaterials

        :type ids: str
        :param ids: JSON list of ids of biomaterials to be synced (default: all)

        :type max_sync: str
        :param max_sync: Maximum number of features to sync (default: all)

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """

        if self.tripal.version == 3:
            raise NotImplementedError("Not possible in Tripal 3. You probably want to use 'entity' -> 'publish' instead.")

        if not job_name:
            job_name = 'Sync Biomaterials'

        if not isinstance(ids, list) and not isinstance(ids, dict):
            ids = json.loads(ids)

        if self.tripal.version == 3:
            raise NotImplementedError("Not yet possible in Tripal 3")

        else:
            job_args = OrderedDict()
            job_args['base_table'] = 'biomaterial'
            job_args['max_sync'] = max_sync
            job_args['organism_id'] = ''
            job_args['types'] = []
            job_args['ids'] = ids
            job_args['linking_table'] = 'chado_biomaterial'
            job_args['node_type'] = 'chado_biomaterial'

            r = self.tripal.job.add_job(job_name, 'chado_biomaterial', 'chado_node_sync_records', job_args)
            if 'job_id' not in r or not r['job_id']:
                raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])
