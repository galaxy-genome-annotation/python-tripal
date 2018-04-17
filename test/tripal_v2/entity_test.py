import unittest

from nose.tools import raises

from . import ti


class EntityTest(unittest.TestCase):

    @raises(NotImplementedError)
    def test_get_entities(self):

        self.ti.entity.get_entities(entity='Analysis')

    @raises(NotImplementedError)
    def test_add_entities(self):

        self.ti.entity.add_entity(entity='Analysis')

    @raises(NotImplementedError)
    def test_get_fields(self):

        self.ti.entity.get_fields(entity='Analysis')

    def setUp(self):
        self.ti = ti
