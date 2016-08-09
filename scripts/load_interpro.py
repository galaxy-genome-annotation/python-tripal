#!/usr/bin/env python
import os
import json
import argparse
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads InterPro results into Tripal (requires tripal_analysis_interpro module)')
    TripalAuth(parser)
    parser.add_argument('interpro', help='Path to the InterProScan file to load (single XML file, or directory containing multiple XML files)')
    parser.add_argument('--analysis-id', type=int, required=True, help='Analysis ID')
    parser.add_argument('--parse-go', action='store_true', help='Load GO terms to the database')
    parser.add_argument('--query-re', help='The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.')
    parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
    parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --query-re regular expression matches unique names instead of names in the database.')

    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Load InterPro results: %s' % os.path.basename(args.gff)

    job_args = [args.analysis_id, args.interpro, int(args.parse_go),
                args.query_re, args.query_type, int(args.query_re_uniquename)]

    print json.dumps(ti.jobs.addJob(job_name, 'tripal_analysis_interpro', 'tripal_analysis_interpro_parseXMLFile', job_args), indent=2)
