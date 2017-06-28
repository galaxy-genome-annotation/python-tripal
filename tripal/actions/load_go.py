#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
from tripal import TripalAuth, TripalAnalysis, TripalInstance


class load_go(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Loads Blast2GO results into Tripal (requires tripal_analysis_go module)')
        TripalAuth(parser)
        TripalAnalysis(parser)
        parser.add_argument('gaf', help='Path to the GAF file to load (single XML file, or directory containing multiple XML files)')
        parser.add_argument('--gaf-ext', help='If looking for files in a directory, extension of the GAF files')
        parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
        parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --re-name regular expression matches unique names instead of names in the database.')
        parser.add_argument('--method', choices=['add', 'remove'], default='add', help='Import method')
        parser.add_argument('--re-name', help='Regular expression to extract the feature name from GAF file.')
        parser.add_argument('--no-wait', action='store_true', help='Do not wait for job to complete')

        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        params = ti.analysis.getBasePayload(args)

        methods = {
            'add': 1,
            'remove': 2,
        }

        params.update({
            'type': 'chado_analysis_go',
            'gaf_file': args.gaf,
            'gaf_file_ext': args.gaf_ext,
            'seq_type': args.query_type,
            'query_uniquename': args.query_uniquename,
            'method': methods[args.method],
            're_name': args.re_name,
            'gojob': 1,
        })

        res = ti.analysis.addAnalysis(params)

        an_node = ti.analysis.getAnalysisNode(res['nid'])
        an_id = an_node['analysis']['analysis_id']
        print("New GO analysis created with ID %s (node id: %s)" % (an_id, res['nid']))
        if not args.no_wait:
            job_id = None
            jobs = ti.jobs.getJobs()
            for job in jobs:
                if job['modulename'] == 'tripal_analysis_go' and job['raw_arguments'][0] == an_id:
                    job_id = job['job_id']
            run_res = ti.jobs.runJobs()
            if not job_id:
                print("Could not get job id for analysis %s" % an_id, file=sys.stderr)
            else:
                ti.jobs.wait(job_id)
                print("Job finished, getting the logs...")
                with open(run_res['stdout'], 'r') as fin:
                    print(fin.read())
                with open(run_res['stderr'], 'r') as fin:
                    print(fin.read(), file=sys.stderr)
