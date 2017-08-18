Tripal Library
==================

.. image:: https://travis-ci.org/abretaud/python-tripal.svg?branch=master
    :target: https://travis-ci.org/abretaud/python-tripal

.. image:: https://readthedocs.org/projects/python-tripal/badge/?version=latest
    :target: http://python-tripal.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

A Python library for interacting with tripal_home_

.. _tripal_home: http://tripal.info/

History
-------

 - 2.0
    - Rewritten most of the code, now working in a similar way as parsec or chakin
    - New cli tool named 'tripaille'
    - Tripal jobs can now be run directly by python-tripal and stdout and stderr are retrieved at the end of jobs.
    - Updated indexing code to latest tripal_elasticsearch module

 - 1.9
    - wait for job completion and get logs

Requirements
------------

The tripal_rest_api_ module needs to be installed on your tripal instance.

.. _tripal_rest_api: http://github.com/abretaud/tripal_rest_api

License
-------

Available under the MIT License
