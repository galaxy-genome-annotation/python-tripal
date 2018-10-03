from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from collections import OrderedDict

from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class EntityClient(Client):
    """Manage any type of Tripal entities"""

    def get_entities(self, entity=None, entity_id=None):
        """
        Get entities

        :type entity: str
        :param entity: Name of the entity type (e.g. Organism)

        :type entity_id: int
        :param entity_id: ID of an entity

        :rtype: list of dict
        :return: Entity information
        """

        if self.tripal.version != 3:
            raise NotImplementedError("Not available in Tripal 2")

        if entity:
            if entity_id:
                entities = [self._get_ws('%s/%s' % (entity, entity_id), {})]
            else:
                entities = [self._get_ws('%s' % (entity), {})]
        else:
            entities = self._get_ws('', {})

        return entities

    def get_bundles(self):
        """
        Get the list of tripal bundles

        :rtype: list of dict
        :return: Bundles information
        """

        if self.tripal.version != 3:
            raise NotImplementedError("Not available in Tripal 2")

        return self._request('entity/list', {})

    def add_entity(self, entity, params={}):
        """
        Add a new entity to the database

        :type entity: str
        :param entity: Name of the entity

        :type params: dict
        :param params: Values to populate the entity fields

        :rtype: dict
        :return: Entity information
        """

        raise NotImplementedError("Waiting for https://github.com/tripal/tripal/issues/202")

        # FIXME This should work, once get_fields is working (gives the expected params structure)
        return self._request_ws(entity, params)

    def publish(self, types=[], job_name=None, no_wait=None):
        """
        Publish entities (Tripal 3 only)

        :type types: list of str
        :param types: List of entity types to be published (e.g. Gene mRNA, default: all)

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """

        if not job_name:
            job_name = 'Publish records'

        if self.tripal.version == 2:
            raise NotImplementedError("Not possible in Tripal 2. You probably want to use 'feature' -> 'sync' instead.")

        bundles = self.tripal.entity.get_bundles()

        bio_data = set()
        if not types:
            bio_data = set(bundles.values())
        else:
            for type in types:
                if type not in bundles:
                    raise Exception("Invalid entity type name: %s, should be one of %s" % (type, set(bundles.keys())))

                bio_data.add(bundles[type])

        jobs_res = []
        for bd in bio_data:
            job_args = OrderedDict()
            job_args[0] = OrderedDict()
            job_args[0]['bundle_name'] = bd
            job_args[0]['filters'] = OrderedDict()  # TODO add support for this, should be a dict with key = field name and value = filter value

            r = self.tripal.job.add_job(job_name, 'tripal_chado', 'chado_publish_records', job_args)
            if 'job_id' not in r or not r['job_id']:
                raise Exception("Failed to create job, received %s" % r)

            if no_wait:
                jobs_res.append(r)
            else:
                run_res = self._run_job_and_wait(r['job_id'])
                if run_res:
                    jobs_res.append(run_res)

        return jobs_res

    def get_fields(self, entity):
        """
        Get the list of available fields for an entity

        :type entity: str
        :param entity: Name of the entity

        :rtype: dict
        :return: Fields information
        """

        raise NotImplementedError("Waiting for https://github.com/tripal/tripal/issues/202")
