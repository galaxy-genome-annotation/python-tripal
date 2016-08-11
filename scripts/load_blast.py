#!/usr/bin/env python
import os
import json
import argparse
from chado import ChadoAuth, ChadoInstance, Analysis, AnalysisProperty, Db
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads Blast results into Tripal (requires tripal_analysis_blast module)')
    TripalAuth(parser)
    parser.add_argument('blast', help='Path to the Blast file to load (single XML file, or directory containing multiple XML files)')
    parser.add_argument('--blast-ext', help='If looking for files in a directory, extension of the blast result files')
    parser.add_argument('--job-name', help='Name of the job (default=\'Load Blast results: <blast_file_name>\')')
    parser.add_argument('--analysis-id', type=int, required=True, help='Analysis ID')
    parser.add_argument('--blastdb', required=True, help='Name of the database blasted against (must be in the Chado db table)')
    parser.add_argument('--blast-parameters', help='Blast parameters used to produce these results')
    parser.add_argument('--max-hits', type=int, default=25, help='Maximum number of hits kept (default=25)')
    parser.add_argument('--query-re', help='The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.')
    parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
    parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --query-re regular expression matches unique names instead of names in the database.')
    parser.add_argument('--is-concat', action='store_true', help='If the blast result file is simply a list of concatenated blast results.')
    parser.add_argument('--search-keywords', action='store_true', help='Extract keywords for Tripal search')

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

    # check if the blastdb exists and get its id
    resdb = ci.session.query(Db).filter_by(name = args.blastdb)

    if not resdb.count():
        raise Exception("Could not find the blastdb %s in the database %s" % (args.blastdb, ci._engine.url))

    blastdb_id = resdb[0].id

    # Add tripal specific properties to the analysis
    props = [
        {'type_name': 'Analysis Type', 'cv_name': 'analysis_property', 'value': 'blast_analysis'},
        {'type_name': 'analysis_blast_blastdb', 'cv_name': 'tripal', 'value': blastdb_id},
        {'type_name': 'analysis_blast_blastfile', 'cv_name': 'tripal', 'value': args.blast},
        {'type_name': 'analysis_blast_blastparameters', 'cv_name': 'tripal', 'value': args.blast-parameters},
        {'type_name': 'analysis_blast_no_parsed', 'cv_name': 'tripal', 'value': args.max_hits},
        {'type_name': 'analysis_blast_query_re', 'cv_name': 'tripal', 'value': args.query_re},
        {'type_name': 'analysis_blast_query_type', 'cv_name': 'tripal', 'value': args.query_type},
        {'type_name': 'analysis_blast_query_uniquename', 'cv_name': 'tripal', 'value': args.query_uniquename},
        {'type_name': 'analysis_blast_blastfile_ext', 'cv_name': 'tripal', 'value': args.blast_ext},
        {'type_name': 'analysis_blast_is_concat', 'cv_name': 'tripal', 'value': int(args.is_concat)},
        {'type_name': 'analysis_blast_search_keywords', 'cv_name': 'tripal', 'value': int(args.search_keywords)}
    ]

    for p in props:
        ap = AnalysisProperty()
        for k, v in p.iteritems():
            ap[k] = v
        ci.session.add(ap)

    ci.session.commit()

    # The analysis is ok, schedule the job
    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Load Blast results: %s' % os.path.basename(args.blast)

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = [args.analysis_id, blastdb_id, args.blast, args.max_hits, args.blast_ext,
                args.query_re, args.query_type, int(args.query_uniquename), int(args.is_concat),
                int(args.search_keywords)]

    r = ti.jobs.addJob(job_name, 'tripal_analysis_blast', 'tripal_analysis_blast_parseXMLFile', job_args)
    print 'Job scheduled with id %s' % r['job_id']
