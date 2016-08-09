#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize features')
    TripalAuth(parser)
    parser.add_argument('--job-name', help='Name of the job (default=\'Sync Features\')')
    parser.add_argument('--organism-id', type=int, required=True, help='Organism ID')
    parser.add_argument('--max-sync', type=int, help='Maximum number of features to sync (default: all)')
    parser.add_argument('--types', nargs='*', help='Space-delimited list of types of records to be synced (e.g. gene mRNA, default: all)')
    parser.add_argument('--ids', nargs='*', help='Space-delimited list of names of records to be synced (e.g. gene0001, default: all)')
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Sync Features'

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = OrderedDict()
    job_args['base_table'] = 'feature'
    job_args['max_sync'] = args.max_sync
    job_args['organism_id'] = args.organism_id
    job_args['types'] = args.types
    job_args['ids'] = args.ids
    job_args['linking_table'] = 'chado_feature'
    job_args['node_type'] = 'chado_feature'

    print json.dumps(ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args), indent=2)
