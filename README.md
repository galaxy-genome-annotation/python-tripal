# Tripal Library

[![Build](https://travis-ci.org/galaxy-genome-annotation/python-tripal.svg?branch=master)](https://travis-ci.org/galaxy-genome-annotation/python-tripal)
[![Documentation](https://readthedocs.org/projects/python-tripal/badge/?version=latest)](http://python-tripal.readthedocs.io/en/latest/?badge=latest)

A Python library for interacting with [Tripal](http://tripal.info/)

## History

 - 3.0
    - Added some support for Tripal 3
        - Add `job add_import_job` for generic Tripal 3 importer
        - Add preliminary code for entity management (waiting for https://github.com/tripal/tripal/issues/202)
        - sync and delete_orphans are not yet implemented (https://github.com/tripal/tripal/issues/337)
    - GFF3: removed bugged 'refresh' and 'remove' loading mode (no more available in Tripal3)
    - Renamed `organism get_organism_nodes` to `organism get_organisms_tripal`
      and `analysis get_analysis_nodes` to `analysis get_analyses_tripal`.
      Both now return Drupal Nodes for Tripal 2 or Entities for Tripal 3.
    - Added `delete_orphans` methods for organisms and analyses
    - Added tests

 - 2.0.4
    - Small bug fixes

 - 2.0.3
    - More reliable detection of job failures

 - 2.0.2
    - Fix broken pip install tripal

 - 2.0.1
    - Fix missing requirements

 - 2.0
    - Rewritten most of the code, now working in a similar way as parsec or chakin
    - New cli tool named 'tripaille'
    - Tripal jobs can now be run directly by python-tripal and stdout and stderr are retrieved at the end of jobs.
    - Updated indexing code to latest tripal_elasticsearch module

 - 1.9
    - Wait for job completion and get logs

## Requirements

The [tripal_rest_api](http://github.com/abretaud/tripal_rest_api) module needs to be installed on your tripal instance.

## License

Available under the MIT License
