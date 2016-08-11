#!/usr/bin/env python
import os
import json
import argparse
from chado import ChadoAuth, ChadoInstance, Analysis, AnalysisProperty, Db
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads InterPro results into Tripal (requires tripal_analysis_interpro module)')
    TripalAuth(parser)
    parser.add_argument('interpro', help='Path to the InterProScan file to load (single XML file, or directory containing multiple XML files)')
    parser.add_argument('--job-name', help='Name of the job (default=\'Load InterPro results: <interpro_file_name>\')')
    parser.add_argument('--analysis-id', type=int, required=True, help='Analysis ID')
    parser.add_argument('--interpro-parameters', help='InterProScan parameters used to produce these results')
    parser.add_argument('--parse-go', action='store_true', help='Load GO terms to the database')
    parser.add_argument('--query-re', help='The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.')
    parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
    parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --query-re regular expression matches unique names instead of names in the database.')

    # Some options to connect directly to chado db using python-chado
    ChadoAuth(parser)

    args = parser.parse_args()

    # We need to modify the analysis first
    ci = ChadoInstance(args.dbhost, args.dbname, args.dbuser, args.dbpass, args.dbschema, args.debug)

    ci.connect()

    # check if the analysis exists
    res = ci.session.query(Analysis).filter_by(analysis_id = args.analysis_id)

    if not res.count():
        raise Exception("Could not find the analysis %s in the database %s" % (args.analysis_id, ci._engine.url))

    # Add tripal specific properties to the analysis
    props = [
        {'type_name': 'Analysis Type', 'cv_name': 'analysis_property', 'value': 'interpro_analysis'},
        {'type_name': 'analysis_interpro_interprofile', 'cv_name': 'tripal', 'value': args.interpro},
        {'type_name': 'analysis_interpro_interproparameters', 'cv_name': 'tripal', 'value': args.interpro_parameters},
        {'type_name': 'analysis_interpro_parsego', 'cv_name': 'tripal', 'value': int(args.parse_go)},
        {'type_name': 'analysis_interpro_query_re', 'cv_name': 'tripal', 'value': args.query_re},
        {'type_name': 'analysis_interpro_query_type', 'cv_name': 'tripal', 'value': args.query_type},
        {'type_name': 'analysis_interpro_query_uniquename', 'cv_name': 'tripal', 'value': args.query_uniquename}
    ]

    for p in props:
        ap = AnalysisProperty()
        for k, v in p.iteritems():
            ap[k] = v
        ci.session.add(ap)

    ci.session.commit()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Load InterPro results: %s' % os.path.basename(args.interpro)

    job_args = [args.analysis_id, args.interpro, int(args.parse_go),
                args.query_re, args.query_type, int(args.query_uniquename)]

    r = ti.jobs.addJob(job_name, 'tripal_analysis_interpro', 'tripal_analysis_interpro_parseXMLFile', job_args)
    print 'Job scheduled with id %s' % r['job_id']
