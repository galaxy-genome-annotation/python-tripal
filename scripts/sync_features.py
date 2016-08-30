#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from chado import ChadoAuth, ChadoInstance, Organism
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize features')
    TripalAuth(parser)
    parser.add_argument('--job-name', help='Name of the job (default=\'Sync Features\')')
    parser.add_argument('--organism', required=True, help='Organism common name')
    parser.add_argument('--max-sync', type=int, help='Maximum number of features to sync (default: all)')
    parser.add_argument('--types', nargs='*', help='Space-delimited list of types of records to be synced (e.g. gene mRNA, default: all)')
    parser.add_argument('--ids', nargs='*', help='Space-delimited list of names of records to be synced (e.g. gene0001, default: all)')

    ChadoAuth(parser)
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    ci = ChadoInstance(args.dbhost, args.dbname, args.dbuser, args.dbpass, args.dbschema, args.debug)
    ci.connect()

    # check if the organism exists and get its id
    resdb = ci.session.query(Organism).filter_by(common_name = args.organism)
    if not resdb.count():
        raise Exception("Could not find the organism %s in the database %s" % (args.organism, ci._engine.url))
    organism_id = resdb.one().organism_id

    job_name = args.job_name
    if not job_name:
        job_name = 'Sync Features'

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = OrderedDict()
    job_args['base_table'] = 'feature'
    job_args['max_sync'] = args.max_sync
    job_args['organism_id'] = organism_id
    job_args['types'] = args.types
    job_args['ids'] = args.ids
    job_args['linking_table'] = 'chado_feature'
    job_args['node_type'] = 'chado_feature'

    r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
    print 'Sync features job scheduled with id %s' % r['job_id']
