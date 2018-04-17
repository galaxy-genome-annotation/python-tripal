import unittest

from . import ci
from . import ti


class OrganismTest(unittest.TestCase):

    def test_add_organism(self):

        genus = "Testus"
        common = "Testorg"
        abbr = "Ttesta"
        species = "testa"
        comment = "A test org"

        org = self.ti.organism.add_organism(genus=genus, common=common, abbr=abbr, species=species, comment=comment)

        assert int(org["nid"]) > 0, "org properly created"

        org = self.ti.organism.get_organisms(abbr=abbr)[0]

        assert org["genus"] == genus, "org properly created"
        assert org["common_name"] == common, "org properly created"
        assert org["abbreviation"] == abbr, "org properly created"
        assert org["species"] == species, "org properly created"
        assert org["comment"] == comment, "org properly created"

        org = self.ti.organism.get_organisms_tripal()

        assert len(org) > 0, "org node properly created"

        found_org = False
        for org in org:
            if org['title'] == '%s %s' % (genus, species):
                found_org = True

        assert found_org, "org node properly created"

    def test_get_taxonomic_ranks(self):

        taxes = self.ti.organism.get_taxonomic_ranks()

        assert len(taxes) > 0, "got some taxonomic_ranks"

        ks = taxes[0].keys()

        assert 'cvterm_id' in ks, 'got correct taxonomic_ranks structure'
        assert 'cv_id' in ks, 'got correct taxonomic_ranks structure'
        assert 'name' in ks, 'got correct taxonomic_ranks structure'
        assert 'definition' in ks, 'got correct taxonomic_ranks structure'
        assert 'dbxref_id' in ks, 'got correct taxonomic_ranks structure'
        assert 'is_obsolete' in ks, 'got correct taxonomic_ranks structure'
        assert 'is_relationshiptype' in ks, 'got correct taxonomic_ranks structure'

    def test_sync_organism(self):

        genus = "Testus 2"
        common = "Testorg 2"
        abbr = "Ttesta 2"
        species = "testa 2"
        comment = "A test org 2"

        org = self.ci.organism.add_organism(genus=genus, common=common, abbr=abbr, species=species, comment=comment)

        org = self.ti.organism.get_organisms(abbr=abbr)[0]

        org_chado_id = org['organism_id']

        assert org["genus"] == genus, "org properly created"
        assert org["common_name"] == common, "org properly created"
        assert org["abbreviation"] == abbr, "org properly created"
        assert org["species"] == species, "org properly created"
        assert org["comment"] == comment, "org properly created"

        org = self.ti.organism.get_organisms_tripal()

        found_org = False
        for org in org:
            if org['title'] == '%s %s' % (genus, species):
                found_org = True

        assert found_org is False, "org not yet synced"

        org = self.ti.organism.sync(organism_id=org_chado_id)

        org = self.ti.organism.get_organisms_tripal()

        found_org = False
        for org in org:
            if org['title'] == '%s %s' % (genus, species):
                found_org = True

        assert found_org, "org properly synced"

    def setUp(self):
        self.ci = ci
        self.ti = ti

        self.ci.organism.delete_organisms()

        self.ci.session.commit()

    def tearDown(self):
        self.ci.organism.delete_organisms()
        self.ti.organism.delete_orphans()

        self.ci.session.commit()
