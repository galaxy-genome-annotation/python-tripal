from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
from collections import OrderedDict
from datetime import datetime

from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class AnalysisClient(Client):
    """Manage Tripal analyses"""

    def get_analyses_tripal(self, analysis_id=None):
        """
        Get analysis entities

        :type analysis_id: int
        :param analysis_id: An analysis entity/node ID

        :rtype: list of dict
        :return: Analysis entity/node information
        """

        if self.tripal.version == 3:
            if analysis_id:
                entities = [self._get_ws('Analysis/%s' % analysis_id, {})]
            else:
                entities = self._get_ws('Analysis', {})
        else:
            if analysis_id:
                entities = [self._get('node/%s' % analysis_id, {})]
            else:
                entities = self._get('node', {})

            entities = [n for n in entities if n['type'].startswith('chado_analysis')]

        return entities

    def get_analyses(self, analysis_id=None, name=None, program=None, programversion=None,
                     algorithm=None, sourcename=None, sourceversion=None,
                     sourceuri=None, date_executed=None):
        """
        Get analyses

        :type analysis_id: str
        :param analysis_id: An analysis ID

        :type name: str
        :param name: analysis name

        :type program: str
        :param program: analysis program

        :type programversion: str
        :param programversion: analysis programversion

        :type algorithm: str
        :param algorithm: analysis algorithm

        :type sourcename: str
        :param sourcename: analysis sourcename

        :type sourceversion: str
        :param sourceversion: analysis sourceversion

        :type sourceuri: str
        :param sourceuri: analysis sourceuri

        :type date_executed: str
        :param date_executed: analysis date_executed (yyyy-mm-dd)

        :rtype: list of dict
        :return: Analysis information
        """

        ans = self._request('chado/list', {'table': 'analysis'})

        if analysis_id:
            ans = [v for v in ans if v['analysis_id'] == str(analysis_id)]
        if name:
            ans = [v for v in ans if v['name'] == name]
        if program:
            ans = [v for v in ans if v['program'] == program]
        if programversion:
            ans = [v for v in ans if v['programversion'] == programversion]
        if algorithm:
            ans = [v for v in ans if v['algorithm'] == algorithm]
        if sourcename:
            ans = [v for v in ans if v['sourcename'] == sourcename]
        if sourceversion:
            ans = [v for v in ans if v['sourceversion'] == sourceversion]
        if sourceuri:
            ans = [v for v in ans if v['sourceuri'] == sourceuri]
        if date_executed:
            ans = [v for v in ans if v['timeexecuted'].startswith(date_executed)]

        return ans

    def add_analysis(self, name, program, programversion, sourcename, algorithm=None,
                     sourceversion=None, sourceuri=None, description=None, date_executed=None):
        """
        Create an analysis

        :type name: str
        :param name: analysis name

        :type program: str
        :param program: analysis program

        :type programversion: str
        :param programversion: analysis programversion

        :type algorithm: str
        :param algorithm: analysis algorithm

        :type sourcename: str
        :param sourcename: analysis sourcename

        :type sourceversion: str
        :param sourceversion: analysis sourceversion

        :type sourceuri: str
        :param sourceuri: analysis sourceuri

        :type description: str
        :param description: analysis description

        :type date_executed: str
        :param date_executed: analysis date_executed (yyyy-mm-dd)

        :rtype: dict
        :return: Analysis information
        """

        date = datetime.today()
        if date_executed:
            date = datetime.strptime(date_executed, '%Y-%m-%d')

        if self.tripal.version == 3:
            params = {
                'entity_type': 'Analysis',
                'params': {
                    'name': name,
                    'software': program,
                    'version_number': programversion,
                    'algorithm': algorithm,
                    'source_data': {
                        'sourcename': sourcename,
                        'sourceversion': sourceversion,
                        'sourceuri': sourceuri,
                    },
                    'description': description,
                    'time_executed': date.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }

            return self._request('entity/create', params)
        else:
            params = {
                'type': 'chado_analysis',
                'analysisname': name,
                'program': program,
                'programversion': programversion,
                'algorithm': algorithm,
                'sourcename': sourcename,
                'sourceversion': sourceversion,
                'sourceuri': sourceuri,
                'description': description,
                'timeexecuted': {
                    'day': date.strftime('%d'),
                    'month': date.strftime('%m'),
                    'year': date.strftime('%Y')
                },
            }

            return self._request('node', params)

    def delete_orphans(self, job_name=None, no_wait=None):
        """
        Delete orphans Drupal analysis nodes

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """

        if not job_name:
            job_name = 'Delete orphan analyses'

        job_args = OrderedDict()
        job_args[0] = 'analysis'
        job_args[1] = 250000
        job_args[2] = 'chado_analysis'
        job_args[3] = 'chado_analysis'

        r = self.tripal.job.add_job(job_name, 'chado_analysis', 'chado_cleanup_orphaned_nodes', job_args)
        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def load_blast(self, name, program, programversion, sourcename, blast_output,
                   blast_ext=None, blastdb=None, blastdb_id=None,
                   blast_parameters=None, query_re=None, query_type=None,
                   query_uniquename=False, is_concat=False, search_keywords=False,
                   no_parsed="all", no_wait=False, algorithm=None, sourceversion=None,
                   sourceuri=None, description=None, date_executed=None):
        """
        Create a Blast analysis

        :type name: str
        :param name: analysis name

        :type program: str
        :param program: analysis program

        :type programversion: str
        :param programversion: analysis programversion

        :type sourcename: str
        :param sourcename: analysis sourcename

        :type blast_output: str
        :param blast_output: Path to the Blast file to load (single XML file, or directory containing multiple XML files)

        :type blast_ext: str
        :param blast_ext: If looking for files in a directory, extension of the blast result files

        :type blastdb: str
        :param blastdb: Name of the database blasted against (must be in the Chado db table)

        :type blastdb_id: str
        :param blastdb_id: ID of the database blasted against (must be in the Chado db table)

        :type blast_parameters: str
        :param blast_parameters: Blast parameters used to produce these results

        :type query_re: str
        :param query_re: The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.

        :type query_type: str
        :param query_type: The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.

        :type query_uniquename: bool
        :param query_uniquename: Use this if the --query-re regular expression matches unique names instead of names in the database.

        :type is_concat: bool
        :param is_concat: If the blast result file is simply a list of concatenated blast results.

        :type search_keywords: bool
        :param search_keywords: Extract keywords for Tripal search

        :type no_parsed: str
        :param no_parsed: Maximum number of hits to parse per feature. Default=all

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :type algorithm: str
        :param algorithm: analysis algorithm

        :type sourceversion: str
        :param sourceversion: analysis sourceversion

        :type sourceuri: str
        :param sourceuri: analysis sourceuri

        :type description: str
        :param description: analysis description

        :type date_executed: str
        :param date_executed: analysis date_executed (yyyy-mm-dd)

        :rtype: str
        :return: Loading information
        """

        if blastdb_id:
            found_db = self.tripal.db.get_dbs(db_id=blastdb_id)
            if not found_db:
                raise Exception("Invalid db ID")
        elif blastdb:
            found_db = self.tripal.db.get_dbs(name=blastdb)
            if not found_db:
                raise Exception("Invalid db name")

            blastdb_id = found_db[0]['db_id']

        if not blastdb_id:
            raise Exception("Either blastdb or blastdb_id is required")

        if self.tripal.version == 3:
            # Tripal v3.x
            if description:
                description += '<br/ >'
            description += 'Blast parameters: {}'.format(blast_parameters)

            analysis = self.add_analysis(name,
                                         program,
                                         programversion,
                                         sourcename,
                                         algorithm,
                                         sourceversion,
                                         sourceuri,
                                         description,
                                         date_executed)

            if not analysis or '@id' not in analysis:
                raise Exception("Failed to create analysis: %s" % analysis)

            an_chado = self.get_analyses(program=program, programversion=programversion, sourcename=sourcename)

            an_id = an_chado[0]['analysis_id']

            job_args = {
                'analysis_id': an_id,
                'blastdb': blastdb_id,
                'blastfile_ext': blast_ext,
                'is_concat': int(is_concat),
                'no_parsed': no_parsed,
                'query_re': query_re,
                'query_type': query_type,
                'query_uniquename': query_uniquename,
            }

            job_name = 'Import Blast file: %s' % os.path.basename(blast_output)

            r = self.tripal.job.add_import_job(job_name, 'BlastImporter', blast_output, job_args)

            if no_wait:
                return r

            if 'job_id' not in r or not r['job_id']:
                raise Exception("Failed to create job, received %s" % r)

            job_id = r['job_id']
        else:
            # Tripal v2.x
            date = datetime.today()
            if date_executed:
                date = datetime.strptime(date_executed, '%Y-%m-%d')

            params = {
                'type': 'chado_analysis_blast',
                'analysisname': name,
                'program': program,
                'programversion': programversion,
                'algorithm': algorithm,
                'sourcename': sourcename,
                'sourceversion': sourceversion,
                'sourceuri': sourceuri,
                'description': description,
                'timeexecuted': {
                    'day': date.strftime('%d'),
                    'month': date.strftime('%m'),
                    'year': date.strftime('%Y')
                },

                'blastdb': blastdb_id,
                'blastfile': blast_output,
                'blastfile_ext': blast_ext,
                'blastjob': 1,  # no reason to not launch a job
                'blastparameters': blast_parameters,
                'query_re': query_re,
                'query_type': query_type,
                'query_uniquename': query_uniquename,
                'is_concat': int(is_concat),
                'search_keywords': int(search_keywords),
            }

            res = self._request('node', params)

            an_node = self.get_analyses_tripal(res['nid'])

            if not an_node:
                raise Exception("Could not find analysis node with id %s" % res['nid'])

            an_node = an_node[0]

            if no_wait:
                return an_node
            else:
                an_id = an_node['analysis']['analysis_id']
                job_id = None
                jobs = self.tripal.job.get_jobs()
                for job in jobs:
                    if job['modulename'] == 'tripal_analysis_blast' and job['raw_arguments'][0] == an_id:
                        job_id = job['job_id']

                if not job_id:
                    raise Exception("Could not get job id for analysis %s" % an_id)

        return self._run_job_and_wait(job_id)

    def load_interpro(self, name, program, programversion, sourcename,
                      interpro_output, interpro_parameters=None, query_re=None,
                      query_type=None, query_uniquename=False, parse_go=False,
                      no_wait=False, algorithm=None, sourceversion=None, sourceuri=None,
                      description=None, date_executed=None):
        """
        Create an Interpro analysis

        :type name: str
        :param name: analysis name

        :type program: str
        :param program: analysis program

        :type programversion: str
        :param programversion: analysis programversion

        :type sourcename: str
        :param sourcename: analysis sourcename

        :type interpro_output: str
        :param interpro_output: Path to the InterProScan file to load (single XML file, or directory containing multiple XML files)

        :type interpro_parameters: str
        :param interpro_parameters: InterProScan parameters used to produce these results

        :type query_re: str
        :param query_re: The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.

        :type query_type: str
        :param query_type: The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.

        :type query_uniquename: bool
        :param query_uniquename: Use this if the query_re regular expression matches unique names instead of names in the database.

        :type parse_go: bool
        :param parse_go: Load GO annotation to the database

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :type algorithm: str
        :param algorithm: analysis algorithm

        :type sourceversion: str
        :param sourceversion: analysis sourceversion

        :type sourceuri: str
        :param sourceuri: analysis sourceuri

        :type description: str
        :param description: analysis description

        :type date_executed: str
        :param date_executed: analysis date_executed (yyyy-mm-dd)

        :rtype: str
        :return: Loading information
        """

        if self.tripal.version == 3:
            # Tripal v3.x
            if description:
                description += '<br/ >'
            description += 'InterProScan parameters: {}'.format(interpro_parameters)

            analysis = self.add_analysis(name,
                                         program,
                                         programversion,
                                         sourcename,
                                         algorithm,
                                         sourceversion,
                                         sourceuri,
                                         description,
                                         date_executed)

            if not analysis or '@id' not in analysis:
                raise Exception("Failed to create analysis: %s" % analysis)

            an_chado = self.get_analyses(program=program, programversion=programversion, sourcename=sourcename)

            an_id = an_chado[0]['analysis_id']

            job_args = {
                'analysis_id': an_id,
                'parsego': int(parse_go),
                'query_re': query_re,
                'query_type': query_type,
                'query_uniquename': query_uniquename,
            }

            job_name = 'Import InterProScan file: %s' % os.path.basename(interpro_output)

            r = self.tripal.job.add_import_job(job_name, 'InterProImporter', interpro_output, job_args)

            if no_wait:
                return r

            if 'job_id' not in r or not r['job_id']:
                raise Exception("Failed to create job, received %s" % r)

            job_id = r['job_id']
        else:
            # Tripal v2.x
            date = datetime.today()
            if date_executed:
                date = datetime.strptime(date_executed, '%Y-%m-%d')

            params = {
                'type': 'chado_analysis_interpro',
                'analysisname': name,
                'program': program,
                'programversion': programversion,
                'algorithm': algorithm,
                'sourcename': sourcename,
                'sourceversion': sourceversion,
                'sourceuri': sourceuri,
                'description': description,
                'timeexecuted': {
                    'day': date.strftime('%d'),
                    'month': date.strftime('%m'),
                    'year': date.strftime('%Y')
                },

                'interprofile': interpro_output,
                'interprojob': 1,
                'parsego': int(parse_go),
                'interproparameters': interpro_parameters,
                'query_re': query_re,
                'query_type': query_type,
                'query_uniquename': query_uniquename,
            }

            res = self._request('node', params)

            an_node = self.get_analyses_tripal(res['nid'])

            if not an_node:
                raise Exception("Could not find analysis node with id %s" % res['nid'])

            an_node = an_node[0]

            if no_wait:
                return an_node
            else:
                an_id = an_node['analysis']['analysis_id']
                job_id = None
                jobs = self.tripal.job.get_jobs()
                for job in jobs:
                    if job['modulename'] == 'tripal_analysis_interpro' and job['raw_arguments'][0] == an_id:
                        job_id = job['job_id']

                if not job_id:
                    raise Exception("Could not get job id for analysis %s" % an_id)

        return self._run_job_and_wait(job_id)

    def load_go(self, name, program, programversion, sourcename, gaf_output,
                organism=None, organism_id=None,
                gaf_ext=None, query_type=None, query_matching='uniquename',
                method='add', name_column=2, re_name=None, no_wait=False, algorithm=None,
                sourceversion=None, sourceuri=None, description=None, date_executed=None):
        """
        Create a GO analysis

        :type organism: str
        :param organism: Organism common name or abbreviation

        :type organism_id: int
        :param organism_id: Organism ID

        :type name: str
        :param name: analysis name

        :type program: str
        :param program: analysis program

        :type programversion: str
        :param programversion: analysis programversion

        :type sourcename: str
        :param sourcename: analysis sourcename

        :type gaf_output: str
        :param gaf_output: Path to the GAF file to load (single file, or directory containing multiple GAF files)

        :type gaf_ext: str
        :param gaf_ext: If looking for files in a directory, extension of the GAF files

        :type query_type: str
        :param query_type: The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.

        :type query_matching: str
        :param query_matching: Method to match identifiers to features in the database. ('name', 'uniquename' or 'dbxref')

        :type method: str
        :param method: Import method ('add' or 'remove')

        :type name_column: int
        :param name_column: Column containing the feature identifiers (2, 3, 10 or 11; default=2).

        :type re_name: str
        :param re_name: Regular expression to extract the feature name from GAF file.

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :type algorithm: str
        :param algorithm: analysis algorithm

        :type sourceversion: str
        :param sourceversion: analysis sourceversion

        :type sourceuri: str
        :param sourceuri: analysis sourceuri

        :type description: str
        :param description: analysis description

        :type date_executed: str
        :param date_executed: analysis date_executed (yyyy-mm-dd)

        :rtype: str
        :return: Loading information
        """

        if organism_id:
            found_org = self.tripal.organism.get_organisms(organism_id=organism_id)
            if not found_org:
                raise Exception("Invalid organism ID")
        elif organism:
            found_org = self.tripal.organism.get_organisms(common=organism)
            if not found_org:
                found_org = self.tripal.organism.get_organisms(abbr=organism)

            if not found_org:
                raise Exception("Invalid organism name")

            organism_id = found_org[0]['organism_id']

        if not organism_id:
            raise Exception("Either organism or organism_id is required")

        methods = {
            'add': 1,
            'remove': 2,
        }

        query_types = OrderedDict()
        query_types['name'] = 'name'
        query_types['uniquename'] = 'uniquename'
        query_types['dbxref'] = 'dbxref'

        if method not in methods:
            raise Exception("Method should be 'add' or 'remove'")

        if query_matching not in query_types:
            raise Exception("Method should be 'name', 'uniquename' or 'dbxref'")

        if self.tripal.version == 3:
            # Tripal v3.x

            analysis = self.add_analysis(name,
                                         program,
                                         programversion,
                                         sourcename,
                                         algorithm,
                                         sourceversion,
                                         sourceuri,
                                         description,
                                         date_executed)

            if not analysis or '@id' not in analysis:
                raise Exception("Failed to create analysis: %s" % analysis)

            an_chado = self.get_analyses(program=program, programversion=programversion, sourcename=sourcename)

            an_id = an_chado[0]['analysis_id']

            job_args = {
                'organism_id': organism_id,
                'analysis_id': an_id,
                'gaf_file_ext': gaf_ext,
                'seq_type': query_type,
                'query_type': query_matching,
                'method': methods[method],
                'name_col': name_column,
                're_name': re_name,
            }

            job_name = 'Import GAF file: %s' % os.path.basename(gaf_output)

            r = self.tripal.job.add_import_job(job_name, 'GAFImporter', gaf_output, job_args)

            if no_wait:
                return r

            if 'job_id' not in r or not r['job_id']:
                raise Exception("Failed to create job, received %s" % r)

            job_id = r['job_id']
        else:
            # Tripal v2.x
            date = datetime.today()
            if date_executed:
                date = datetime.strptime(date_executed, '%Y-%m-%d')

            params = {
                'type': 'chado_analysis_go',
                'analysisname': name,
                'program': program,
                'programversion': programversion,
                'algorithm': algorithm,
                'sourcename': sourcename,
                'sourceversion': sourceversion,
                'sourceuri': sourceuri,
                'description': description,
                'timeexecuted': {
                    'day': date.strftime('%d'),
                    'month': date.strftime('%m'),
                    'year': date.strftime('%Y')
                },

                'gaf_file': gaf_output,
                'gaf_file_ext': gaf_ext,
                'seq_type': query_type,
                'query_uniquename': (query_matching == 'uniquename'),
                'method': methods[method],
                're_name': re_name,
                'gojob': 1,
            }

            res = self._request('node', params)

            an_node = self.get_analyses_tripal(res['nid'])

            if not an_node:
                raise Exception("Could not find analysis node with id %s" % res['nid'])

            an_node = an_node[0]

            if no_wait:
                return an_node
            else:
                an_id = an_node['analysis']['analysis_id']
                job_id = None
                jobs = self.tripal.job.get_jobs()
                for job in jobs:
                    if job['modulename'] == 'tripal_analysis_go' and job['raw_arguments'][0] == an_id:
                        job_id = job['job_id']

                if not job_id:
                    raise Exception("Could not get job id for analysis %s" % an_id)

        return self._run_job_and_wait(job_id)

    def load_fasta(self, fasta, organism=None, organism_id=None, analysis=None,
                   analysis_id=None, sequence_type="contig", re_name=None,
                   re_uniquename=None, db_ext_id=None, re_accession=None,
                   rel_type=None, rel_subject_re=None, rel_subject_type=None,
                   method='insup', match_type='uniquename', job_name=None, no_wait=False):
        """
        Load fasta sequences

        :type fasta: str
        :param fasta: Path to the Fasta file to load

        :type organism: str
        :param organism: Organism common name or abbreviation

        :type organism_id: int
        :param organism_id: Organism ID

        :type analysis: str
        :param analysis: Analysis name

        :type analysis_id: int
        :param analysis_id: Analysis ID

        :type sequence_type: str
        :param sequence_type: Sequence type

        :type re_name: str
        :param re_name: Regular expression for the name

        :type re_uniquename: str
        :param re_uniquename: Regular expression for the unique name

        :type db_ext_id: str
        :param db_ext_id: External DB ID

        :type re_accession: str
        :param re_accession: Regular expression for the accession from external DB

        :type rel_type: str
        :param rel_type: Relation type (part_of or derives_from)

        :type rel_subject_re: str
        :param rel_subject_re: Relation subject regular expression (used to extract id of related entity)

        :type rel_subject_type: str
        :param rel_subject_type: Relation subject type (must match already loaded data, e.g. mRNA)

        :type method: str
        :param method: Insertion method (insert, update or insup, default=insup (Insert and Update))

        :type match_type: str
        :param match_type: Match type for already loaded features (name or uniquename; default=uniquename; used for "Update only" or "Insert and update" methods)'

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :rtype: str
        :return: Loading information
        """

        if organism_id:
            found_org = self.tripal.organism.get_organisms(organism_id=organism_id)
            if not found_org:
                raise Exception("Invalid organism ID")
        elif organism:
            found_org = self.tripal.organism.get_organisms(common=organism)
            if not found_org:
                found_org = self.tripal.organism.get_organisms(abbr=organism)

            if not found_org:
                raise Exception("Invalid organism name")

            organism_id = found_org[0]['organism_id']

        if not organism_id:
            raise Exception("Either organism or organism_id is required")

        if analysis_id:
            found_an = self.get_analyses(analysis_id=analysis_id)
            if not found_an:
                raise Exception("Invalid analysis ID")
        elif analysis:
            found_an = self.get_analyses(name=analysis)

            if not found_an:
                raise Exception("Invalid analysis name")

            analysis_id = found_an[0]['analysis_id']

        if not analysis_id:
            raise Exception("Either analysis or analysis_id is required")

        methods = OrderedDict()
        methods['insert'] = 'Insert only'
        methods['update'] = 'Update only'
        methods['insup'] = 'Insert and update'

        if method not in methods:
            raise Exception("Method should be 'insert', 'update', or 'insup'")

        rel_types = {
            'part_of': 'part_of',
            'derives_from': 'derives_from',
        }

        if rel_type and rel_type not in rel_types:
            raise Exception("rel_type should be 'part_of' or 'derives_from'")
        elif rel_type:
            rel_type = rel_types[rel_type]

        match_types = OrderedDict()
        match_types['name'] = 'Name'
        match_types['uniquename'] = 'Unique name'

        if match_type not in match_types:
            raise Exception("match_type should be 'name' or 'uniquename'")

        if not job_name:
            job_name = 'Import FASTA file: %s' % os.path.basename(fasta)

        if self.tripal.version == 3:
            # Tripal v3.x
            job_args = {
                'analysis_id': analysis_id,
                'organism_id': organism_id,
                'seqtype': sequence_type,
                'method': list(methods.keys()).index(method),
                'match_type': list(match_types.keys()).index(match_type),
                're_name': re_name,
                're_uname': re_uniquename,
                're_accession': re_accession,
                'db_id': db_ext_id,
                'rel_type': rel_type,
                're_subject': rel_subject_re,
                'parent_type': rel_subject_type,
            }

            r = self.tripal.job.add_import_job(job_name, 'FASTAImporter', fasta, job_args)
        else:
            # Tripal v2.x
            uid = 1  # user id is not really used by the loader, 1 is admin user

            job_args = [fasta, organism_id, sequence_type, re_name, re_uniquename, re_accession,
                        db_ext_id, rel_type, rel_subject_re, rel_subject_type,
                        methods[method], uid, analysis_id, match_types[match_type]]

            r = self.tripal.job.add_job(job_name, 'tripal_feature', 'tripal_feature_load_fasta', job_args)

        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def load_gff3(self, gff, organism=None, organism_id=None, analysis=None,
                  analysis_id=None, import_mode='update', target_organism=None,
                  target_organism_id=None, target_type=None, target_create=False,
                  start_line=None, landmark_type=None, alt_id_attr=None,
                  create_organism=None, re_mrna=None, re_protein=None, job_name=None, no_wait=False):
        """
        Load GFF3 file

        :type gff: str
        :param gff: Path to the GFF file to load

        :type organism: str
        :param organism: Organism common name or abbreviation

        :type organism_id: int
        :param organism_id: Organism ID

        :type analysis: str
        :param analysis: Analysis name

        :type analysis_id: int
        :param analysis_id: Analysis ID

        :type import_mode: str
        :param import_mode: Import mode (add_only=existing features won't be touched, update=existing features will be updated and obsolete attributes kept)')

        :type target_organism: str
        :param target_organism: In case of Target attribute in the GFF3, choose the organism abbreviation or common name to which target sequences belong. Select this only if target sequences belong to a different organism than the one specified with --organism-id. And only choose an organism here if all of the target sequences belong to the same species. If the targets in the GFF file belong to multiple different species then the organism must be specified using the 'target_organism=genus:species' attribute in the GFF file.')

        :type target_organism_id: int
        :param target_organism_id: In case of Target attribute in the GFF3, choose the organism ID to which target sequences belong. Select this only if target sequences belong to a different organism than the one specified with --organism-id. And only choose an organism here if all of the target sequences belong to the same species. If the targets in the GFF file belong to multiple different species then the organism must be specified using the \'target_organism=genus:species\' attribute in the GFF file.')

        :type target_type: str
        :param target_type: In case of Target attribute in the GFF3, if the unique name for a target sequence is not unique (e.g. a protein and an mRNA have the same name) then you must specify the type for all targets in the GFF file. If the targets are of different types then the type must be specified using the \'target_type=type\' attribute in the GFF file. This must be a valid Sequence Ontology (SO) term.')

        :type target_create: bool
        :param target_create: In case of Target attribute in the GFF3, if the target feature cannot be found, create one using the organism and type specified above, or using the \'target_organism\' and \'target_type\' fields specified in the GFF file. Values specified in the GFF file take precedence over those specified above.')

        :type start_line: int
        :param start_line: The line in the GFF file where importing should start

        :type landmark_type: str
        :param landmark_type: A Sequence Ontology type for the landmark sequences in the GFF fie (e.g. \'chromosome\').

        :type alt_id_attr: str
        :param alt_id_attr: When ID attribute is absent, specify which other attribute can uniquely identify the feature.

        :type create_organism: bool
        :param create_organism: Create organisms when encountering organism attribute (these lines will be skip otherwise)

        :type re_mrna: str
        :param re_mrna: Regular expression for the mRNA name

        :type re_protein: str
        :param re_protein: Replacement string for the protein name

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :rtype: str
        :return: Loading information
        """

        if organism_id:
            found_org = self.tripal.organism.get_organisms(organism_id=organism_id)
            if not found_org:
                raise Exception("Invalid organism ID")
        elif organism:
            found_org = self.tripal.organism.get_organisms(common=organism)
            if not found_org:
                found_org = self.tripal.organism.get_organisms(abbr=organism)

            if not found_org:
                raise Exception("Invalid organism name")

            organism_id = found_org[0]['organism_id']

        if not organism_id:
            raise Exception("Either organism or organism_id is required")

        if analysis_id:
            found_an = self.get_analyses(analysis_id=analysis_id)
            if not found_an:
                raise Exception("Invalid analysis ID")
        elif analysis:
            found_an = self.get_analyses(name=analysis)

            if not found_an:
                raise Exception("Invalid analysis name")

            analysis_id = found_an[0]['analysis_id']

        if not analysis_id:
            raise Exception("Either analysis or analysis_id is required")

        if target_organism_id:
            found_torg = self.tripal.organism.get_organisms(organism_id=target_organism_id)
            if not found_torg:
                raise Exception("Invalid target organism ID")
        elif target_organism:
            found_torg = self.tripal.organism.get_organisms(common=target_organism)
            if not found_torg:
                found_torg = self.tripal.organism.get_organisms(abbr=target_organism)

            if not found_torg:
                raise Exception("Invalid target organism name")

            target_organism_id = found_torg[0]['organism_id']

        import_modes = OrderedDict()
        import_modes['add_only'] = 'add_only'
        import_modes['update'] = 'update'

        if import_mode not in import_modes:
            raise Exception("import_mode should be 'add_only', 'update'")

        if not job_name:
            job_name = 'Import GFF3 file: %s' % os.path.basename(gff)

        transaction = 1  # use transaction or not, no reason to disable this

        if self.tripal.version == 3:
            # Tripal v3.x
            job_args = {
                'analysis_id': analysis_id,
                'organism_id': organism_id,
                'line_number': str(start_line),
                'landmark_type': landmark_type,
                'alt_id_attr': alt_id_attr,
                're_mrna': re_mrna,
                're_protein': re_protein,
                'use_transaction': transaction,
                'add_only': int(import_mode == 'add_only'),
                'update': int(import_mode == 'update'),
                'create_organism': int(create_organism),
                'target_organism_id': target_organism_id,
                'target_type': target_type,
                'create_target': int(target_create),
            }

            r = self.tripal.job.add_import_job(job_name, 'GFF3Importer', gff, job_args)
        else:
            job_args = [gff, organism_id, analysis_id, int(import_mode == 'add_only'),
                        int(import_mode == 'update'), 0, 0,
                        transaction, target_organism_id, target_type, int(target_create), start_line,
                        landmark_type, alt_id_attr, int(create_organism), re_mrna, re_protein]

            r = self.tripal.job.add_job(job_name, 'tripal_feature', 'tripal_feature_load_gff3', job_args)

        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def sync(self, analysis=None, analysis_id=None, job_name=None, no_wait=None):
        """
        Synchronize an analysis

        :type analysis: str
        :param analysis: Analysis name

        :type analysis_id: str
        :param analysis_id: ID of the analysis to sync

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """

        if analysis_id:
            found_an = self.get_analyses(analysis_id=analysis_id)
            if not found_an:
                raise Exception("Invalid analysis ID")
        elif analysis:
            found_an = self.get_analyses(name=analysis)
            if not found_an:
                raise Exception("Invalid analysis name")

            analysis_id = found_an[0]['analysis_id']

        if not analysis_id:
            raise Exception("Either analysis or analysis_id is required")

        if not job_name:
            job_name = 'Sync Analysis'

        job_args = OrderedDict()
        job_args['base_table'] = 'analysis'
        job_args['max_sync'] = ''
        job_args['organism_id'] = ''
        job_args['types'] = []
        job_args['ids'] = [int(analysis_id)]
        job_args['linking_table'] = 'chado_analysis'
        job_args['node_type'] = 'chado_analysis'

        r = self.tripal.job.add_job(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])
