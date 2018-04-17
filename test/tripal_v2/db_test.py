import unittest

from . import ti


class DbTest(unittest.TestCase):

    def test_get_dbs(self):

        dbs = self.ti.db.get_dbs()

        assert len(dbs) > 0, "got some dbs"

        ks = dbs[0].keys()

        assert 'db_id' in ks, 'got correct db structure'
        assert 'name' in ks, 'got correct db structure'
        assert 'description' in ks, 'got correct db structure'
        assert 'urlprefix' in ks, 'got correct db structure'
        assert 'url' in ks, 'got correct db structure'

    def test_get_mviews(self):

        mviews = self.ti.db.get_mviews()

        assert len(mviews) > 0, "got some mviews"

        ks = mviews[0].keys()

        assert 'mview_id' in ks, 'got correct mview structure'
        assert 'name' in ks, 'got correct mview structure'
        assert 'modulename' in ks, 'got correct mview structure'
        assert 'mv_table' in ks, 'got correct mview structure'
        assert 'mv_specs' in ks, 'got correct mview structure'
        assert 'mv_schema' in ks, 'got correct mview structure'
        assert 'indexed' in ks, 'got correct mview structure'
        assert 'query' in ks, 'got correct mview structure'
        assert 'special_index' in ks, 'got correct mview structure'
        assert 'last_update' in ks, 'got correct mview structure'
        assert 'status' in ks, 'got correct mview structure'
        assert 'comment' in ks, 'got correct mview structure'

    # TODO test index()
    # TODO test populate_mviews()

    def setUp(self):
        self.ti = ti
