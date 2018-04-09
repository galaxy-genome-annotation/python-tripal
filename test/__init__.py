from chado import ChadoInstance
from tripaille.config import get_instance

ti = get_instance('test_local')
ci = ChadoInstance(dbuser="postgres", dbpass="postgres", dbname="postgres", dbschema="chado")


def setup_package():
    global ti
    global ci
