#!/usr/bin/env python
import os
import json
import argparse
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads Blast results into Tripal (requires tripal_analysis_blast module)')
    TripalAuth(parser)
    parser.add_argument('blast', help='Path to the Blast file to load (single XML file, or directory containing multiple XML files)')
    parser.add_argument('--blast-ext', help='If looking for files in a directory, extension of the blast result files')
    parser.add_argument('--job-name', help='Name of the job (default=\'Load Blast results: <blast_file_name>\')')
    parser.add_argument('--analysis-id', type=int, required=True, help='Analysis ID')
    parser.add_argument('--blastdb-id', type=int, required=True, help='ID of the database blasted against')
    parser.add_argument('--max-hits', type=int, required=True, default=25, help='Maximum number of hits kept (default=25)')
    parser.add_argument('--query-re', help='The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.')
    parser.add_argument('--query-type', help='The feature type (e.g. \'gene\', \'mRNA\', \'contig\') of the query. It must be a valid Sequence Ontology term.')
    parser.add_argument('--query-uniquename', action='store_true', help='Use this if the --query-re regular expression matches unique names instead of names in the database.')
    parser.add_argument('--is-concat', action='store_true', help='If the blast result file is simply a list of concatenated blast results.')
    parser.add_argument('--search-keywords', action='store_true', help='Extract keywords for Tripal search')

    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Load Blast results: %s' % os.path.basename(args.gff)

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = [args.analysis_id, args.blastdb_id, args.blast, args.max_hits, args.blast_ext,
                args.query_re, args.query_type, int(args.query_re_uniquename), int(args.is_concat),
                int(args.search_keywords)]

    print json.dumps(ti.jobs.addJob(job_name, 'tripal_analysis_blast', 'tripal_analysis_blast_parseXMLFile', job_args), indent=2)
