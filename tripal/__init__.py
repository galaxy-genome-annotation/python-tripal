from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import logging
from tripal.analysis import AnalysisClient
from tripal.db import DbClient
from tripal.feature import FeatureClient
from tripal.job import JobClient
from tripal.organism import OrganismClient

from future import standard_library
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

        self.analysis = AnalysisClient(self)
        self.db = DbClient(self)
        self.feature = FeatureClient(self)
        self.job = JobClient(self)
        self.organism = OrganismClient(self)

    def __str__(self):
        return '<TripalInstance at %s>' % self.tripal_url
