#!/usr/bin/env python
import json
import argparse
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

    job_args = {
                    'base_table': 'analysis',
                    'max_sync': '',
                    'organism_id': '',
                    'types': '',
                    'ids': [args.analysis_id],
                    'linking_table': 'chado_analysis',
                    'node_type': 'chado_analysis'
                }

    print json.dumps(ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args), indent=2)
