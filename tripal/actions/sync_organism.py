#!/usr/bin/env python
from __future__ import print_function
import argparse
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance


class sync_organism(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Synchronize organism')
        TripalAuth(parser)
        parser.add_argument('--job-name', help='Name of the job (default=\'Sync Organism\')')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--organism', help='Organism abbreviation or common name')
        group.add_argument('--organism-id', help='Organism ID')

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
            job_name = 'Sync Organism'

        job_args = OrderedDict()
        job_args['base_table'] = 'organism'
        job_args['max_sync'] = ''
        job_args['organism_id'] = ''
        job_args['types'] = []
        job_args['ids'] = [org_id]
        job_args['linking_table'] = 'chado_organism'
        job_args['node_type'] = 'chado_organism'

        r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
        print('Sync organism job scheduled with id %s' % r['job_id'])
