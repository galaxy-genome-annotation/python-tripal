#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance


class sync_analysis(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Synchronize analysis')
        TripalAuth(parser)
        parser.add_argument('--job-name', help='Name of the job (default=\'Sync Analysis\')')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--analysis', help='Analysis name')
        group.add_argument('--analysis-id', help='Analysis ID')
        parser.add_argument('--no-wait', action='store_true', help='Do not wait for job to complete')

        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        an_id = None
        if args.analysis:
            an_id = ti.analysis.getAnalysisByName(args.analysis)['analysis_id']
        elif args.analysis_id:
            an_id = args.analysis_id
        else:
            raise Exception("Either --analysis or --analysis-id is required")

        job_name = args.job_name
        if not job_name:
            job_name = 'Sync Analysis'

        job_args = OrderedDict()
        job_args['base_table'] = 'analysis'
        job_args['max_sync'] = ''
        job_args['organism_id'] = ''
        job_args['types'] = []
        job_args['ids'] = [int(an_id)]
        job_args['linking_table'] = 'chado_analysis'
        job_args['node_type'] = 'chado_analysis'

        r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
        print('Sync analysis job scheduled with id %s' % r['job_id'])

        if not args.no_wait:
            run_res = ti.jobs.runJobs()
            ti.jobs.wait(r['job_id'])
            with open(run_res['stdout'], 'r') as fin:
                print(fin.read())
            with open(run_res['stderr'], 'r') as fin:
                print(fin.read(), file=sys.stderr)
