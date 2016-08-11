#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize analysis')
    TripalAuth(parser)
    parser.add_argument('--job-name', help='Name of the job (default=\'Sync Analysis\')')
    parser.add_argument('--analysis-id', type=int, required=True, help='Analysis ID')
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Sync Analysis'

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = OrderedDict()
    job_args['base_table'] = 'analysis'
    job_args['max_sync'] = ''
    job_args['organism_id'] = ''
    job_args['types'] = []
    job_args['ids'] = [args.analysis_id]
    job_args['linking_table'] = 'chado_analysis'
    job_args['node_type'] = 'chado_analysis'

    r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
    print 'Job scheduled with id %s' % r.job_id
