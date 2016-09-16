#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance

class sync_features(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Synchronize features')
        TripalAuth(parser)
        parser.add_argument('--job-name', help='Name of the job (default=\'Sync Features\')')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--organism', help='Organism abbreviation or common name')
        group.add_argument('--organism-id', help='Organism ID')
        parser.add_argument('--max-sync', type=int, help='Maximum number of features to sync (default: all)')
        parser.add_argument('--types', nargs='*', help='Space-delimited list of types of records to be synced (e.g. gene mRNA, default: all)')
        parser.add_argument('--ids', nargs='*', help='Space-delimited list of names of records to be synced (e.g. gene0001, default: all)')

        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        org_id = None
        if args.organism:
            org_id = ti.organism.getOrganismByName(args.organism)['organism_id']
        elif args.organism_id:
            org_id = args.organism_id
        else:
            raise Exception("Either --organism or --organism-id is required")

        job_name = args.job_name
        if not job_name:
            job_name = 'Sync Features'

        transaction = 1 # use transaction or not, no reason to disable this

        job_args = OrderedDict()
        job_args['base_table'] = 'feature'
        job_args['max_sync'] = args.max_sync
        job_args['organism_id'] = org_id
        job_args['types'] = args.types
        job_args['ids'] = args.ids
        job_args['linking_table'] = 'chado_feature'
        job_args['node_type'] = 'chado_feature'

        r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
        print 'Sync features job scheduled with id %s' % r['job_id']
