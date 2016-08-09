#!/usr/bin/env python
import json
import argparse
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

    job_args = {
                    'base_table': 'organism',
                    'max_sync': '',
                    'organism_id': '',
                    'types': '',
                    'ids': [args.organism_id],
                    'linking_table': 'chado_organism',
                    'node_type': 'chado_organism'
                }

    print json.dumps(ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args), indent=2)
