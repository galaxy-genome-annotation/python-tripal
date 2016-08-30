#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from chado import ChadoAuth, ChadoInstance, Analysis
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize analysis')
    TripalAuth(parser)
    parser.add_argument('--job-name', help='Name of the job (default=\'Sync Analysis\')')
    parser.add_argument('--analysis', required=True, help='Analysis name')

    ChadoAuth(parser)
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    ci = ChadoInstance(args.dbhost, args.dbname, args.dbuser, args.dbpass, args.dbschema, args.debug)
    ci.connect()

    # check if the analysis exists and get its id
    resdb = ci.session.query(Analysis).filter_by(name = args.analysis)
    if not resdb.count():
        raise Exception("Could not find the analysis %s in the database %s" % (args.analysis, ci._engine.url))
    analysis_id = resdb.one().analysis_id

    job_name = args.job_name
    if not job_name:
        job_name = 'Sync Analysis'

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = OrderedDict()
    job_args['base_table'] = 'analysis'
    job_args['max_sync'] = ''
    job_args['organism_id'] = ''
    job_args['types'] = []
    job_args['ids'] = [analysis_id]
    job_args['linking_table'] = 'chado_analysis'
    job_args['node_type'] = 'chado_analysis'

    r = ti.jobs.addJob(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
    print 'Sync analysis job scheduled with id %s' % r['job_id']
