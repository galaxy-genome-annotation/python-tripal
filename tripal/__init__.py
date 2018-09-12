from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from future import standard_library

import requests

from tripal.analysis import AnalysisClient
from tripal.biomaterial import BiomaterialClient
from tripal.db import DbClient
from tripal.entity import EntityClient
from tripal.expression import ExpressionClient
from tripal.feature import FeatureClient
from tripal.job import JobClient
from tripal.organism import OrganismClient
from tripal.phylogeny import PhylogenyClient

standard_library.install_aliases()

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class TripalInstance(object):

    def __init__(self, tripal_url="http://localhost/tripal/", username="admin", password="changeme", auth_login=None, auth_password=None, **kwargs):

        self.tripal_url = tripal_url
        self.username = username
        self.password = password

        self.auth_login = auth_login
        self.auth_password = auth_password

        self.version = self._get_tripal_version()

        self.analysis = AnalysisClient(self)
        self.db = DbClient(self)
        self.entity = EntityClient(self)
        self.feature = FeatureClient(self)
        self.job = JobClient(self)
        self.organism = OrganismClient(self)
        self.phylogeny = PhylogenyClient(self)
        self.biomaterial = BiomaterialClient(self)
        self.expression = ExpressionClient(self)

    def __str__(self):
        return '<TripalInstance at %s>' % self.tripal_url

    def _get_tripal_version(self):
        url = self.tripal_url + 'web-services/'  # This api is only available in Tripal > 3.0

        auth = None
        if self.auth_login and self.auth_password:
            auth = (self.auth_login, self.auth_password)

        r = requests.get(url, auth=auth)

        try:
            ws_desc = r.json()

            if r.status_code == 200 and '@context' in ws_desc:
                return 3
        except (ValueError, KeyError):
            return 2

        return 2
