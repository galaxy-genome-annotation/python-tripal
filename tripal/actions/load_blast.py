#!/usr/bin/env python
import os
import json
import argparse
from tripal import TripalAuth, TripalAnalysis, TripalInstance

class load_blast(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Loads Blast results into Tripal (requires tripal_analysis_blast module)')
        TripalAuth(parser)
        TripalAnalysis(parser)
        parser.add_argument('blast', help='Path to the Blast file to load (single XML file, or directory containing multiple XML files)')
        parser.add_argument('--blast-ext', help='If looking for files in a directory, extension of the blast result files')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--blastdb', help='Name of the database blasted against (must be in the Chado db table)')
        group.add_argument('--blastdb-id', help='ID of the database blasted against (must be in the Chado db table)')
        parser.add_argument('--blast-parameters', help='Blast parameters used to produce these results')
        parser.add_argument('--max-hits', type=int, default=25, help='Maximum number of hits kept (default=25)')
        parser.add_argument('--query-re', help='The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.')
        parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
        parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --query-re regular expression matches unique names instead of names in the database.')
        parser.add_argument('--is-concat', action='store_true', help='If the blast result file is simply a list of concatenated blast results.')
        parser.add_argument('--search-keywords', action='store_true', help='Extract keywords for Tripal search')

        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        blastdb_id = None
        if args.blastdb:
            blastdb_id = ti.db.getDbByName(args.blastdb)['db_id']
        elif args.blastdb_id:
            blastdb_id = args.blastdb_id
        else:
            raise Exception("Either --blastdb or --blastdb-id is required")

        params = ti.analysis.getBasePayload(args)

        params.update({
            'type': 'chado_analysis_blast',
            'blastdb': blastdb_id,
            'blastfile': args.blast,
            'blastfile_ext': args.blast_ext,
            'blastjob': 1, # no reason to not launch a job
            'blastparameters': args.blast_parameters,
            'query_re': args.query_re,
            'query_type': args.query_type,
            'query_uniquename': args.query_uniquename,
            'is_concat': int(args.is_concat),
            'search_keywords': int(args.search_keywords),
        })

        res = ti.analysis.addAnalysis(params)

        print "New Blast analysis created with ID: %s" % res['nid']
