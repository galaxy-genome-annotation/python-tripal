import unittest

from nose.tools import raises

from . import ti


class EntityTest(unittest.TestCase):

    def test_get_entities(self):

        ents = self.ti.entity.get_entities(entity='Analysis')

        assert len(ents) == 1, "Got collection of entities"

        ents = ents[0]

        assert '@context' in ents, "Got collection of entities"
        assert '@id' in ents, "Got collection of entities"
        assert '@type' in ents, "Got collection of entities"
        assert 'label' in ents, "Got collection of entities"
        assert 'totalItems' in ents, "Got collection of entities"

        assert ents['@type'] == 'Analysis_Collection', "Got collection of entities"
        assert ents['label'] == 'Analysis Collection', "Got collection of entities"

    @raises(NotImplementedError)
    def test_add_entities(self):

        self.ti.entity.add_entity(entity='Analysis')

    @raises(NotImplementedError)
    def test_get_fields(self):

        self.ti.entity.get_fields(entity='Analysis')

    def setUp(self):
        self.ti = ti
