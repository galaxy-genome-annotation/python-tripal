from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from collections import OrderedDict
import logging
from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class OrganismClient(Client):
    CLIENT_BASE = '/tripal_api/'

    def get_organism_nodes(self, node=None):
        """
        Get organism nodes

        :type node: int
        :param node: filter on node id

        :rtype: list of dict
        :return: Organism node information
        """

        if node:
            nodes = [self._get('node/%s' % node, {})]
        else:
            nodes = self._get('node', {})

        nodes = [n for n in nodes if n['type'] == 'chado_organism']

        return nodes

    def get_organisms(self, organism_id=None, genus=None, species=None, common=None, abbr=None,
                      comment=None):
        """
        Get organisms

        :type organism_id: str
        :param organism_id: An organism ID

        :type genus: str
        :param genus: The genus of the organism

        :type common: str
        :param common: The common name of the organism

        :type abbr: str
        :param abbr: The abbreviation of the organism

        :type species: str
        :param species: The species of the organism

        :type comment: str
        :param comment: A comment / description

        :rtype: list of dict
        :return: Organism information
        """

        orgs = self._request('chado/list', {'table': 'organism'})
        if organism_id:
            orgs = [v for v in orgs if v['organism_id'] == str(organism_id)]
        if genus:
            orgs = [v for v in orgs if v['genus'] == genus]
        if species:
            orgs = [v for v in orgs if v['species'] == species]
        if common:
            orgs = [v for v in orgs if v['common_name'] == common]
        if abbr:
            orgs = [v for v in orgs if v['abbreviation'] == abbr]
        if comment:
            orgs = [v for v in orgs if v['comment'] == comment]

        return orgs

    def add_organism(self, genus, common, abbr, species=None, comment=None,
                     infraspecific_rank=None, infraspecific_name=None):
        """
        Add a new organism to the database

        :type genus: str
        :param genus: The genus of the organism

        :type common: str
        :param common: The common name of the organism

        :type abbr: str
        :param abbr: The abbreviation of the organism

        :type species: str
        :param species: The species of the organism

        :type comment: str
        :param comment: A comment / description

        :type infraspecific_rank: str
        :param infraspecific_rank: The type name of infraspecific name for any taxon below the rank of species. Must be one of ['subspecies', 'varietas', 'subvariety', 'forma', 'subforma']

        :type infraspecific_name: str
        :param infraspecific_name: The infraspecific name for this organism.

        :rtype: dict
        :return: Organism information
        """

        if (infraspecific_rank or infraspecific_name) and not (infraspecific_name and infraspecific_rank):
            raise Exception("You should specific both infraspecific_rank and infraspecific_name, or none of them.")

        if infraspecific_rank and infraspecific_rank not in ['subspecies', 'varietas', 'subvariety', 'forma', 'subforma']:
            raise Exception("infraspecific_rank must be one of ['subspecies', 'varietas', 'subvariety', 'forma', 'subforma']")

        params = {
            'type': 'chado_organism',
            'genus': genus,
            'species': species,
            'abbreviation': abbr,
            'common_name': common,
            'description': {
                'value': comment
            },
            'type_id': 0,
            'infraspecific_name': '',
        }

        if infraspecific_rank:
            params['infraspecific_name'] = infraspecific_name
            allowed_ranks = self.get_taxonomic_ranks()

            for r in allowed_ranks:
                if r['name'] == infraspecific_rank:
                    params['type_id'] = int(r['cvterm_id'])
                    break

        return self._request('node', params)

    def get_taxonomic_ranks(self):
        """
        Get taxonomic ranks

        :rtype: list of dict
        :return: Taxonomic ranks
        """

        return self._request('chado/taxonomic_ranks', {})

    def sync(self, organism=None, organism_id=None, job_name=None, no_wait=None):
        """
        Synchronize an organism

        :type organism: str
        :param organism: Common name of the organism to sync

        :type organism_id: str
        :param organism_id: ID of the organism to sync

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """

        if organism_id:
            found_org = self.get_organisms(organism_id=organism_id)
            if not found_org:
                raise Exception("Invalid organism ID")
        elif organism:
            found_org = self.get_organisms(common=organism)
            if not found_org:
                found_org = self.get_organisms(abbr=organism)

            if not found_org:
                raise Exception("Invalid organism name")

            organism_id = found_org[0]['organism_id']

        if not organism_id:
            raise Exception("Either organism or organism_id is required")

        if not job_name:
            job_name = 'Sync Organism'

        job_args = OrderedDict()
        job_args['base_table'] = 'organism'
        job_args['max_sync'] = ''
        job_args['organism_id'] = ''
        job_args['types'] = []
        job_args['ids'] = [organism_id]
        job_args['linking_table'] = 'chado_organism'
        job_args['node_type'] = 'chado_organism'

        r = self.tripal.job.add_job(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])
