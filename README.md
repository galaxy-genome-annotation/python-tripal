# Tripal Library

[![Build](https://travis-ci.org/galaxy-genome-annotation/python-tripal.svg?branch=master)](https://travis-ci.org/galaxy-genome-annotation/python-tripal)
[![Documentation](https://readthedocs.org/projects/python-tripal/badge/?version=latest)](http://python-tripal.readthedocs.io/en/latest/?badge=latest)

A Python library for interacting with [Tripal](http://tripal.info/).

It allows to load data into a remote Tripal instance, and explore its content, directly from Python code, or using a CLI (Command Line Interface).

See below for examples of what you can do using the `tripal` python module, and the `tripaille` CLI.

(in case you wonder: Tripaille's name comes from a bad french word play)

## Requirements

The [tripal_rest_api](http://github.com/abretaud/tripal_rest_api) module needs to be installed on your Tripal instance (choose the master branch for Tripal 2, or the branch 7.x-3.x for Tripal 3).

## Installation

```bash
$ pip install tripal

# On first use you'll need to create a config file to connect to the tripal server, just run:

$ tripaille init
Welcome to Tripal's Tripaille!
TRIPAL_URL: http://localhost/
TRIPAL_USER: admin
TRIPAL_PASS: changeme
```

This will create a tripaille config file in ~/.tripaille.yml

## Examples

```python
    from tripal import TripalInstance
    ti = TripalInstance(tripal_url='http://localhost:8500/', username='admin', password='changeme')

    # Create human species
    org = ti.organism.add_organism(genus="Homo", species="sapiens", common="Human", abbr="H.sapiens")

    # Then display the list of organisms
    orgs = ti.organism.get_organisms()

    for org in orgs:
        print('{} {}'.format(org['genus'], org['species']))

    # Create an analysis
    an = ti.analysis.add_analysis(name="My cool analysis",
                                       program="Something",
                                       programversion="1.0",
                                       algorithm="Google",
                                       sourcename="src",
                                       sourceversion="2.1beta",
                                       sourceuri="http://example.org/",
                                       date_executed="2018-02-03")

    # Then display the list of organisms
    ans = ti.analysis.get_analyses()

    # And load some data
    ti.analysis.load_fasta(fasta="./test-data/Citrus_sinensis-scaffold00001.fasta", analysis_id=ans[0]['analysis_id'], organism_id=orgs[0]['organism_id'])
    ti.analysis.load_gff3(gff="./test-data/Citrus_sinensis-orange1.1g015632m.g.gff3", analysis_id=ans[0]['analysis_id'], organism_id=orgs[0]['organism_id'])
```

Or with the Tripaille client:

```bash
    $ tripaille organism add_organism --abbr H.sapiens --common Human Homo sapiens

    $ tripaille organism get_organisms
    [
        {
            "organism_id": "17",
            "abbreviation": "H.sapiens",
            "genus": "Homo",
            "species": "sapiens",
            "common_name": "Human",
            "infraspecific_name": null,
            "type_id": null,
            "comment": ""
        }
    ]

    # Then load some data
    $ tripaille analysis add_analysis \
        "My cool analysis" \
        "Something" \
        "v1.0" \
        "src"


    $ tripaille analysis get_analyses
    [
        {
            "analysis_id": "68",
            "name": "My cool analysis",
            "description": "",
            "program": "Something",
            "programversion": "1.0",
            "timeexecuted": "2018-02-03 00:00:00"
        },
    ]

    $ tripaille analysis load_fasta \
        --analysis_id 68 \
        --sequence_type contig \
        --organism_id 17 \
        ./test-data/Citrus_sinensis-scaffold00001.fasta
```

## History

 - 3.2.1
    - Fix error when loading blast or interpro with empty description

 - 3.2
    - Fix support for elasticsearch indexing with Tripal 3

 - 3.1.1
    - Minor release to fix broken package at pypi, no code change

 - 3.1
    - Add expression module to manage biomaterials and expression data (with tripal_expression module)
    - Add entity.get_bundles() and entity.publish() methods for Tripal 3

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

## License

Available under the MIT License
