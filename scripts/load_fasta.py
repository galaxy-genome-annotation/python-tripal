#!/usr/bin/env python
import os
import json
import argparse
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads a fasta file into Tripal')
    TripalAuth(parser)
    parser.add_argument('fasta', help='Path to the fasta file to load')
    parser.add_argument('--job-name', help='Name of the job (default=\'Import FASTA file: <fasta_file_name>\')')
    parser.add_argument('--organism-id', type=int, required=True, help='Organism ID')
    parser.add_argument('--analysis-id', type=int, required=True, help='Analysis ID')
    parser.add_argument('--sequence-type', help='Sequence type (default: contig)', default='contig')
    parser.add_argument('--re-name', help='Regular expression for the name', default='')
    parser.add_argument('--re-uniquename', help='Regular expression for the unique name', default='')
    parser.add_argument('--db-ext-id', help='External DB ID', default='')
    parser.add_argument('--re-accession', help='Regular expression for the accession from external DB', default='')
    parser.add_argument('--rel-type', help='Relation type', choices=['part_of', 'derives_from'], default='')
    parser.add_argument('--rel-subject-re', help='Relation subject regular expression (used to extract id of related entity)', default='')
    parser.add_argument('--rel-subject-type', help='Relation subject type (must match already loaded data, e.g. mRNA)', default='')
    parser.add_argument('--method', help='Insertion method', choices=['Insert only', 'Update only', 'Insert and update'], default='Insert and update')
    parser.add_argument('--match-type', help='Match type for already loaded features (used for "Update only" or "Insert and update" methods)', choices=['Name', 'Unique name'], default='Unique name')
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Import FASTA file: %s' % os.path.basename(args.fasta)

    uid = 1 # user id is not really used by the loader, 1 is admin user

    job_args = [args.fasta, args.organism_id, args.sequence_type, args.re_name, args.re_uniquename, args.re_accession,
                args.db_ext_id, args.rel_type, args.rel_subject_re, args.rel_subject_type,
                args.method, uid, args.analysis_id, args.match_type]

    print json.dumps(ti.jobs.addJob(job_name, 'tripal_feature', 'tripal_feature_load_fasta', job_args), indent=2)


"""
a:14:{
    i:0;
        s:42:\"/test_data/sfru_rice_genome_sample.fa\";
    i:1;
        s:2:\"13\";
    i:2;
        s:4:\"contig\";
    i:3;
        s:0:\"\";
    i:4;
        s:0:\"\";
    i:5;
        s:0:\"\";
    i:6;
        s:0:\"\";
    i:7;
        s:0:\"\";
    i:8;
        s:0:\"\";
    i:9;
        s:0:\"\";
    i:10;
        s:11:\"Update only\";
    i:11;
        s:1:\"1\";
    i:12;
        s:2:\"10\";
    i:13;
        s:11:\"Unique name\";
}"""
