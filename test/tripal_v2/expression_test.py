import unittest

from nose.tools import raises

from . import ci
from . import ti


class ExpressionTest(unittest.TestCase):

    def test_add_biomaterial(self):

        # Setup testing data
        biomaterial_name = "SM130"
        file_path = "/data/Biomaterial.xml"
        file_type = "xml"
        genus = "Testus"
        common = "Testorg"
        abbr = "Ttesta"
        species = "testa"
        comment = "A test org"

        org = self.ti.organism.add_organism(genus=genus, common=common, abbr=abbr, species=species, comment=comment)
        org = self.ti.organism.get_organisms(abbr=abbr)[0]

        org_chado_id = org['organism_id']

        self.ti.expression.add_biomaterial(org_chado_id, file_path, file_type)

        biomat_list = self.ti.expression.get_biomaterials(biomaterial_name=biomaterial_name)

        assert len(biomat_list) == 1, "Issue : Expecting only one biomaterial in list"

        biomat = biomat_list[0]

        assert biomat["name"] == biomaterial_name, "Biomaterial name issue : " + biomat["name"]
        assert biomat["taxon_id"] == org_chado_id, "Organism issue : " + biomat["taxon_id"]

    def test_sync_biomaterials(self):
        # Setup testing data
        biomaterial_name = "SM130"
        file_path = "/data/Biomaterial.xml"
        file_type = "xml"
        genus = "Testus"
        common = "Testorg"
        abbr = "Ttesta"
        species = "testa"
        comment = "A test org"

        org = self.ti.organism.add_organism(genus=genus, common=common, abbr=abbr, species=species, comment=comment)
        org = self.ti.organism.get_organisms(abbr=abbr)[0]

        org_chado_id = org['organism_id']
        self.ti.expression.add_biomaterial(org_chado_id, file_path, file_type)
        biomat_list = self.ti.expression.get_biomaterials(biomaterial_name=biomaterial_name)

        assert len(biomat_list) == 1, "Issue : Expecting only one biomaterial in list"

        biomaterial_id = biomat_list[0]["biomaterial_id"]
        biomat_published_dict = self.ti.expression.get_biomaterials_tripal()

        assert len(biomat_published_dict) == 0, "Error : Number of published biomaterials is not 0"

        self.ti.expression.sync_biomaterials()
        biomat_published_dict = self.ti.expression.get_biomaterials_tripal()
        # In V2, its a list of entity. Just need to check lenght
        assert len(biomat_published_dict) == 1, "Error : Number of published biomaterials is not 1"
        assert biomat_published_dict[0]["title"] == biomaterial_name, "Error : Published biomaterial label does not match"

    def test_add_expression(self):

        # Setup testing data
        # Expression file
        expression_file_path = "/data/Test_expression.matrix"
        # Mock organism
        genus = "Testus"
        common = "Testorg"
        abbr = "Ttesta"
        species = "testa"
        comment = "A test org"
        # Mock analysis
        name = "analysis x"
        program = "Magic"
        programversion = "1.0"
        algorithm = "mind"
        sourcename = "src"
        sourceversion = "2.1beta"
        sourceuri = "http://example.org/"
        description = "Bla bla bla"
        date_executed = "2018-02-03"
        # Feature file (fasta)
        feature_file_path = "/data/Citrus_sinensis-orange1.1g015632m.g.fasta"

        ana = self.ti.analysis.add_analysis(name=name, program=program, programversion=programversion, algorithm=algorithm, sourcename=sourcename, sourceversion=sourceversion, sourceuri=sourceuri, description=description, date_executed=date_executed)
        ana = self.ti.analysis.get_analyses(name=name)[0]
        ana_chado_id = ana['analysis_id']

        org = self.ti.organism.add_organism(genus=genus, common=common, abbr=abbr, species=species, comment=comment)
        org = self.ti.organism.get_organisms(abbr=abbr)[0]
        org_chado_id = org['organism_id']

        # Create the features linked in the expression file
        self.ti.analysis.load_gff3(gff='/data/Citrus_sinensis-orange1.1g015632m.g.gff3', organism_id=org_chado_id, analysis_id=ana_chado_id)
        self.ti.analysis.load_fasta(fasta=feature_file_path, organism_id=org_chado_id, analysis_id=ana_chado_id, sequence_type="mRNA", method='update', match_type='name')

        # Load the expression file

        self.ti.expression.add_expression(org_chado_id, ana_chado_id, expression_file_path)
        biomat_list = self.ti.expression.get_biomaterials()
        # We expect 8 biomaterials to be created

        assert len(biomat_list) == 8, "Unexpected number of biomaterials created"


    def setUp(self):

        self.ci = ci
        self.ti = ti

        self.ci.organism.delete_organisms()
        self.ci.analysis.delete_analyses()
        self.ci.expression.delete_all_biomaterials(confirm=True)
        ci.feature.delete_features()

        self.ci.session.commit()

    def tearDown(self):

        self.ci.organism.delete_organisms()
        self.ci.analysis.delete_analyses()
        self.ci.expression.delete_all_biomaterials(confirm=True)
        ci.feature.delete_features()

        self.ci.session.commit()
