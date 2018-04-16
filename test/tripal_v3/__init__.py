from chakin.config import get_instance as get_instance_chakin
from tripaille.config import get_instance as get_instance_tripaille

ti = get_instance_tripaille('test_local')
ci = get_instance_chakin('test_local')


def setup_package():
    global ti
    global ci
