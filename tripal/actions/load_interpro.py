#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
from tripal import TripalAuth, TripalAnalysis, TripalInstance


class load_interpro(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Loads InterPro results into Tripal (requires tripal_analysis_interpro module)')
        TripalAuth(parser)
        TripalAnalysis(parser)
        parser.add_argument('interpro', help='Path to the InterProScan file to load (single XML file, or directory containing multiple XML files)')
        parser.add_argument('--interpro-parameters', help='InterProScan parameters used to produce these results')
        parser.add_argument('--parse-go', action='store_true', help='Load GO annotation to the database')
        parser.add_argument('--query-re', help='The regular expression that can uniquely identify the query name. This parameters is required if the feature name does not identically match the query name.')
        parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
        parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --query-re regular expression matches unique names instead of names in the database.')
        parser.add_argument('--no-wait', action='store_true', help='Do not wait for job to complete')

        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        params = ti.analysis.getBasePayload(args)

        params.update({
            'type': 'chado_analysis_interpro',
            'interprofile': args.interpro,
            'interprojob': 1,
            'parsego': int(args.parse_go),
            'interproparameters': args.interpro_parameters,
            'query_re': args.query_re,
            'query_type': args.query_type,
            'query_uniquename': args.query_uniquename,
        })

        res = ti.analysis.addAnalysis(params)

        print("New Interpro analysis created with ID: %s" % res['nid'])

        if not args.no_wait:
            run_res = ti.jobs.runJobs()
            ti.jobs.wait(r['job_id'])
            with open(run_res['stdout'], 'r') as fin:
                print(fin.read())
            with open(run_res['stderr'], 'r') as fin:
                print(fin.read(), file=sys.stderr)
