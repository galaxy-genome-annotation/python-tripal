#!/usr/bin/env python
from __future__ import print_function
import os
import argparse
import sys
from tripal import TripalAuth, TripalInstance


class load_fasta(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Loads a fasta file into Tripal')
        TripalAuth(parser)
        parser.add_argument('fasta', help='Path to the fasta file to load')
        parser.add_argument('--job-name', help='Name of the job (default=\'Import FASTA file: <fasta_file_name>\')')
        groupo = parser.add_mutually_exclusive_group(required=True)
        groupo.add_argument('--organism', help='Organism abbreviation or common name')
        groupo.add_argument('--organism-id', help='Organism ID')
        groupa = parser.add_mutually_exclusive_group(required=True)
        groupa.add_argument('--analysis', help='Analysis name')
        groupa.add_argument('--analysis-id', help='Analysis ID')
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
        parser.add_argument('--no-wait', action='store_true', help='Do not wait for job to complete')

        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        org_id = None
        if args.organism:
            org_id = ti.organism.getOrganismByName(args.organism)['organism_id']
        elif args.organism_id:
            org_id = args.organism_id
        else:
            raise Exception("Either --organism or --organism-id is required")

        an_id = None
        if args.analysis:
            an_id = ti.analysis.getAnalysisByName(args.analysis)['analysis_id']
        elif args.analysis_id:
            an_id = args.analysis_id
        else:
            raise Exception("Either --analysis or --analysis-id is required")

        job_name = args.job_name
        if not job_name:
            job_name = 'Import FASTA file: %s' % os.path.basename(args.fasta)

        uid = 1  # user id is not really used by the loader, 1 is admin user

        job_args = [args.fasta, org_id, args.sequence_type, args.re_name, args.re_uniquename, args.re_accession,
                    args.db_ext_id, args.rel_type, args.rel_subject_re, args.rel_subject_type,
                    args.method, uid, an_id, args.match_type]

        r = ti.jobs.addJob(job_name, 'tripal_feature', 'tripal_feature_load_fasta', job_args)
        print('Load fasta job scheduled with id %s' % r['job_id'])

        if not args.no_wait:
            run_res = ti.jobs.runJobs()
            ti.jobs.wait(r['job_id'])
            with open(run_res['stdout'], 'r') as fin:
                print(fin.read())
            with open(run_res['stderr'], 'r') as fin:
                print(fin.read(), file=sys.stderr)
