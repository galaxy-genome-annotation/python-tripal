#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize organism')
    TripalAuth(parser)
    parser.add_argument('--job-name', help='Name of the job (default=\'Sync Organism\')')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--organism', help='Organism abbreviation or common name')
    group.add_argument('--organism-id', help='Organism ID')

    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    org_id = None
    if args.organism:
        org_id = ti.organism.getOrganismByName(args.organism)['organism_id']
    elif args.organism_id:
        org_id = args.organism_id
    else:
        raise Exception("Either --organism or --organism-id is required")

    job_name = args.job_name
    if not job_name:
        job_name = 'Sync Organism'

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = OrderedDict()
    job_args['base_table'] = 'organism'
    job_args['max_sync'] = ''
    job_args['organism_id'] = ''
    job_args['types'] = []
    job_args['ids'] = [org_id]
    job_args['linking_table'] = 'chado_organism'
    job_args['node_type'] = 'chado_organism'

    r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
    print 'Sync organism job scheduled with id %s' % r['job_id']
