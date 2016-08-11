#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize organism')
    TripalAuth(parser)
    parser.add_argument('--job-name', help='Name of the job (default=\'Sync Organism\')')
    parser.add_argument('--organism-id', type=int, required=True, help='Organism ID')
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Sync Organism'

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = OrderedDict()
    job_args['base_table'] = 'organism'
    job_args['max_sync'] = ''
    job_args['organism_id'] = ''
    job_args['types'] = []
    job_args['ids'] = [args.organism_id]
    job_args['linking_table'] = 'chado_organism'
    job_args['node_type'] = 'chado_organism'

    r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
    print 'Job scheduled with id %s' % r.job_id
