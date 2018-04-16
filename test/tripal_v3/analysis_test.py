import unittest

from nose.tools import raises

from . import ci
from . import ti


class AnalysisTest(unittest.TestCase):

    def test_add_analysis(self):

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

        assert ana["@id"].startswith("http://"), "ana properly created"
        assert ana["ItemPage"].startswith("http://"), "ana properly created"

        ana = self.ti.analysis.get_analyses(name=name)[0]

        assert ana["name"] == name, "analysis chado record properly created"
        assert ana["program"] == program, "analysis chado record properly created"
        assert ana["programversion"] == programversion, "analysis chado record properly created"
        assert ana["algorithm"] == algorithm, "analysis chado record properly created"
        assert ana["sourcename"] == sourcename, "analysis chado record properly created"
        assert ana["sourceversion"] == sourceversion, "analysis chado record properly created"
        assert ana["sourceuri"] == sourceuri, "analysis chado record properly created"
        assert ana["description"] == description, "analysis chado record properly created"
        assert ana["timeexecuted"] == '2018-02-03 00:00:00', "analysis chado record properly created"

        ana = self.ti.analysis.get_analyses_tripal()
        assert len(ana) > 0, "ana entity properly created"

        found_an = False
        for an in ana['member']:
            if an['label'] == name:
                found_an = True
                assert an['@type'] == "Analysis", "ana entity properly created"

        assert found_an, "ana entity properly created"

    @raises(NotImplementedError)
    def test_sync_analysis(self):

        name = "analysis x"
        program = "Magic"
        programversion = "1.0"
        algorithm = "mind"
        sourcename = "src"
        sourceversion = "2.1beta"
        sourceuri = "http://example.org/"
        description = "Bla bla bla"
        date_executed = "2018-02-03"

        ana = self.ci.analysis.add_analysis(name=name, program=program, programversion=programversion, algorithm=algorithm, sourcename=sourcename, sourceversion=sourceversion, sourceuri=sourceuri, description=description, date_executed=date_executed)

        assert ana["analysis_id"] > 0, "ana properly created"

        ana = self.ti.analysis.get_analyses(name=name)[0]

        ana_chado_id = ana['analysis_id']

        assert ana["name"] == name, "analysis chado record properly created"
        assert ana["program"] == program, "analysis chado record properly created"
        assert ana["programversion"] == programversion, "analysis chado record properly created"
        assert ana["algorithm"] == algorithm, "analysis chado record properly created"
        assert ana["sourcename"] == sourcename, "analysis chado record properly created"
        assert ana["sourceversion"] == sourceversion, "analysis chado record properly created"
        assert ana["sourceuri"] == sourceuri, "analysis chado record properly created"
        assert ana["description"] == description, "analysis chado record properly created"
        assert ana["timeexecuted"] == '2018-02-03 00:00:00', "analysis chado record properly created"

        ana = self.ti.analysis.get_analyses_tripal()
        print(ana)

        found_ana = False
        for ana in ana['member']:
            if ana['label'] == '%s' % (name):
                found_ana = True

        assert found_ana is False, "ana not yet synced"

        self.ti.analysis.sync(analysis_id=ana_chado_id)

        ana = self.ti.analysis.get_analyses_tripal()

        found_ana = False
        for ana in ana['member']:
            if ana['label'] == '%s' % (name):
                found_ana = True

        assert found_ana, "ana properly synced"

    def setUp(self):
        self.ci = ci
        self.ti = ti

        self.ci.analysis.delete_analyses()

        self.ci.session.commit()

    def tearDown(self):
        self.ci.analysis.delete_analyses()
        # self.ti.analysis.delete_orphans() # TODO uncomment when implemented

        self.ci.session.commit()
