from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
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
            raise NotImplementedError()

        if entity:
            if entity_id:
                entities = [self._get_ws('%s/%s' % (entity, entity_id), {})]
            else:
                entities = [self._get_ws('%s' % (entity), {})]
        else:
            entities = self._get_ws('', {})

        return entities

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

        if self.tripal.version != 3:
            raise NotImplementedError()

        return self._request_ws(entity, params)

    def get_fields(self, entity):
        """
        Get the list of available fields for an entity

        :type entity: str
        :param entity: Name of the entity

        :rtype: dict
        :return: Fields information
        """

        raise NotImplementedError()
