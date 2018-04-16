import sys
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from . import ci
from . import ti


class FeatureTest(unittest.TestCase):

    def test_full_genome(self):

        name = "analysis x"
        program = "Magic"
        programversion = "1.0"
        algorithm = "mind"
        sourcename = "src"
        sourceversion = "2.1beta"
        sourceuri = "http://example.org/"
        description = "Bla bla bla"
        date_executed = "2018-02-03"

        ana = self.ti.analysis.add_analysis(name=name, program=program, programversion=programversion, algorithm=algorithm, sourcename=sourcename, sourceversion=sourceversion, sourceuri=sourceuri, description=description, date_executed=date_executed)

        ana = self.ti.analysis.get_analyses(name=name)[0]

        ana_chado_id = ana['analysis_id']

        genus = "Testus 2"
        common = "Testorg 2"
        abbr = "Ttesta 2"
        species = "testa 2"
        comment = "A test org 2"

        org = self.ci.organism.add_organism(genus=genus, common=common, abbr=abbr, species=species, comment=comment)

        org = self.ti.organism.get_organisms(abbr=abbr)[0]

        org_chado_id = org['organism_id']

        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        try:
            out = StringIO()
            err = StringIO()
            sys.stdout = out
            sys.stderr = err

            self.ti.analysis.load_gff3(gff='/data/Citrus_sinensis-orange1.1g015632m.g.gff3', organism_id=org_chado_id, analysis_id=ana_chado_id)

            output = out.getvalue().strip()
            output_err = err.getvalue().strip()

            assert "Chado GFF3 File Loader" in output, "gff loaded"
            assert "Percent complete: 100.00%." in output, "gff loaded"
            assert "Done" in output, "gff loaded"
            assert "[error]" not in output_err, "gff loaded"
            assert "[ERROR]" not in output_err, "gff loaded"

            out = StringIO()
            err = StringIO()
            sys.stdout = out
            sys.stderr = err

            self.ti.analysis.load_fasta(fasta='/data/Citrus_sinensis-scaffold00001.fasta', organism_id=org_chado_id, analysis_id=ana_chado_id, sequence_type="supercontig", method='update', match_type='name')

            output = out.getvalue().strip()
            output_err = err.getvalue().strip()

            assert "Chado FASTA Loader" in output, "genome loaded"
            assert "Percent complete: 100.00%." in output, "genome loaded"
            assert "Done" in output, "genome loaded"
            assert "[error]" not in output_err, "genome loaded"
            assert "[ERROR]" not in output_err, "genome loaded"

            out = StringIO()
            err = StringIO()
            sys.stdout = out
            sys.stderr = err

            self.ti.analysis.load_fasta(fasta='/data/Citrus_sinensis-orange1.1g015632m.g.fasta', organism_id=org_chado_id, analysis_id=ana_chado_id, sequence_type="mRNA", method='update', match_type='name')

            output = out.getvalue().strip()
            output_err = err.getvalue().strip()

            assert "Chado FASTA Loader" in output, "transcripts loaded"
            assert "Percent complete: 100.00%." in output, "transcripts loaded"
            assert "Done" in output, "transcripts loaded"
            assert "[error]" not in output_err, "transcripts loaded"
            assert "[ERROR]" not in output_err, "transcripts loaded"

            out = StringIO()
            err = StringIO()
            sys.stdout = out
            sys.stderr = err

            db_id = self.ti.db.get_dbs(name="swissprot:display")[0]['db_id']

            self.ti.analysis.load_blast(blast_output='/data/Blastx_citrus_sinensis-orange1.1g015632m.g.fasta.0_vs_uniprot_sprot.fasta.out', name="blastx Citrus sinensis v1.0 genes vs ExPASy SwissProt", sourcename="C. sinensis mRNA vs ExPASy SwissProt", algorithm="blastx", description="Bla bla bla", blastdb_id=db_id, query_type="mRNA", blast_parameters="bla blo blu", program="blastall", programversion="2.2.25")

            output = out.getvalue().strip()
            output_err = err.getvalue().strip()

            assert "Chado BLAST XML results loader" in output, "blast loaded"
            assert "Percent complete: 100.00%." in output, "blast loaded"
            assert "Done" in output, "blast loaded"
            assert "[error]" not in output_err, "blast loaded"
            assert "[ERROR]" not in output_err, "blast loaded"

            out = StringIO()
            err = StringIO()
            sys.stdout = out
            sys.stderr = err

            db_id = self.ti.db.get_dbs(name="genbank:protein")[0]['db_id']

            self.ti.analysis.load_blast(blast_output='/data/Blastx_citrus_sinensis-orange1.1g015632m.g.fasta.0_vs_nr.out', name="blastx Citrus sinensis v1.0 genes vs NCBI nr", sourcename="C. sinensis mRNA vs NCBI nr", algorithm="blastx", description="Bla bla bla", blastdb_id=db_id, query_type="mRNA", blast_parameters="bla blo blu", program="blastall", programversion="2.2.25")

            output = out.getvalue().strip()
            output_err = err.getvalue().strip()

            assert "Chado BLAST XML results loader" in output, "blast loaded"
            assert "Percent complete: 100.00%." in output, "blast loaded"
            assert "Done" in output, "blast loaded"
            assert "[error]" not in output_err, "blast loaded"
            assert "[ERROR]" not in output_err, "blast loaded"

            out = StringIO()
            err = StringIO()
            sys.stdout = out
            sys.stderr = err

            self.ti.analysis.load_interpro(interpro_output='/data/Citrus_sinensis-orange1.1g015632m.g.iprscan.xml', name="InterPro Annotations of C. sinensis v1.0", sourcename="C. sinensis v1.0 mRNA", algorithm="iprscan", description="Bla bla bla", query_type="mRNA", parse_go=True, interpro_parameters="bla blo blu", program="InterProScan", programversion="4.8")

            output = out.getvalue().strip()
            output_err = err.getvalue().strip()

            assert "Chado InterProScan XML results loader" in output, "interpro loaded"
            assert "Percent complete: 100.00%." in output, "interpro loaded"
            assert "Done" in output, "interpro loaded"
            assert "[error]" not in output_err, "interpro loaded"
            assert "[ERROR]" not in output_err, "interpro loaded"

            out = StringIO()
            err = StringIO()
            sys.stdout = out
            sys.stderr = err

            self.ti.analysis.load_go(gaf_output='/data/blast2go.gaf', name="Blast2GO Annotation of C. sinensis v1.0", sourcename="C. sinensis Blast2GO", query_type="polypeptide", program="Blast2GO", programversion="2.5", organism_id=org_chado_id)

            output = out.getvalue().strip()
            output_err = err.getvalue().strip()

            assert "Chado GAF Loader" in output, "gaf loaded"
            assert "Done" in output, "gaf loaded"
            assert "[error]" not in output_err, "gaf loaded"
            assert "[ERROR]" not in output_err, "gaf loaded"
        finally:
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        # Sync data
        # Data was loaded successfully, now, check that it is online

    def setUp(self):
        self.ci = ci
        self.ti = ti

        self.ci.analysis.delete_analyses()
        self.ci.organism.delete_organisms()

        self.ci.session.commit()

    def tearDown(self):
        self.ci.analysis.delete_analyses()
        self.ci.organism.delete_organisms()
        # self.ti.organism.delete_orphans() # TODO uncomment when implemented
        # self.ti.analysis.delete_orphans() # TODO uncomment when implemented

        self.ci.session.commit()
