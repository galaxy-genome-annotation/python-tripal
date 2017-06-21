#!/usr/bin/env python
from __future__ import print_function
import os
import argparse
from tripal import TripalAuth, TripalInstance


class load_gff3(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Loads a GFF3 file into Tripal')
        TripalAuth(parser)
        parser.add_argument('gff', help='Path to the GFF3 file to load')
        parser.add_argument('--job-name', help='Name of the job (default=\'Import GFF3 file: <gff3_file_name>\')')
        groupo = parser.add_mutually_exclusive_group(required=True)
        groupo.add_argument('--organism', help='Organism abbreviation or common name')
        groupo.add_argument('--organism-id', help='Organism ID')
        groupa = parser.add_mutually_exclusive_group(required=True)
        groupa.add_argument('--analysis', help='Analysis name')
        groupa.add_argument('--analysis-id', help='Analysis ID')
        parser.add_argument('--import-mode', choices=['add_only', 'update', 'refresh', 'remove'], default='update', help='Import mode, default=update (add_only=existing features won\'t be touched, update=existing features will be updated and obsolete attributes kept, refresh=existing features will be updated and obsolete attributes removed, remove=features present in the db and in the GFF3 file will be reomved)')
        groupt = parser.add_mutually_exclusive_group()
        groupt.add_argument('--target-organism', help='In case of Target attribute in the GFF3, choose the organism abbreviation or common name to which target sequences belong. Select this only if target sequences belong to a different organism than the one specified with --organism-id. And only choose an organism here if all of the target sequences belong to the same species. If the targets in the GFF file belong to multiple different species then the organism must be specified using the \'target_organism=genus:species\' attribute in the GFF file.')
        groupt.add_argument('--target-organism-id', help='In case of Target attribute in the GFF3, choose the organism ID to which target sequences belong. Select this only if target sequences belong to a different organism than the one specified with --organism-id. And only choose an organism here if all of the target sequences belong to the same species. If the targets in the GFF file belong to multiple different species then the organism must be specified using the \'target_organism=genus:species\' attribute in the GFF file.')
        parser.add_argument('--target-type', help='In case of Target attribute in the GFF3, if the unique name for a target sequence is not unique (e.g. a protein and an mRNA have the same name) then you must specify the type for all targets in the GFF file. If the targets are of different types then the type must be specified using the \'target_type=type\' attribute in the GFF file. This must be a valid Sequence Ontology (SO) term.')
        parser.add_argument('--target-create', action='store_true', help='In case of Target attribute in the GFF3, if the target feature cannot be found, create one using the organism and type specified above, or using the \'target_organism\' and \'target_type\' fields specified in the GFF file. Values specified in the GFF file take precedence over those specified above.')
        parser.add_argument('--start-line', type=int, help='The line in the GFF file where importing should start')
        parser.add_argument('--landmark-type', help='A Sequence Ontology type for the landmark sequences in the GFF fie (e.g. \'chromosome\'). If the GFF file contains a \'##sequence-region\' line that describes the landmark sequences to which all others are aligned and a type is provided here then the features will be created if they do not already exist. If they do exist then this field is not used')
        parser.add_argument('--alt-id-attr', help='Sometimes lines in the GFF file are missing the required ID attribute that specifies the unique name of the feature, but there may be another attribute that can uniquely identify the feature. If so, you may specify the name of the attribute to use for the name.')
        parser.add_argument('--create-organism', action='store_true', help='The Tripal GFF loader supports the "organism" attribute. This allows features of a different organism to be aligned to the landmark sequence of another species. The format of the attribute is "organism=[genus]:[species]", where [genus] is the organism\'s genus and [species] is the species name. Check this box to automatically add the organism to the database if it does not already exists. Otherwise lines with an organism attribute where the organism is not present in the database will be skipped.')
        parser.add_argument('--re-mrna', help='Regular expression for the mRNA name')
        parser.add_argument('--re-protein', help='Replacement string for the protein name')

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

        target_org_id = None
        if args.target_organism:
            target_org_id = ti.organism.getOrganismByName(args.organism)['organism_id']
        elif args.target_organism_id:
            target_org_id = args.organism_id

        job_name = args.job_name
        if not job_name:
            job_name = 'Import GFF3 file: %s' % os.path.basename(args.gff)

        transaction = 1  # use transaction or not, no reason to disable this

        job_args = [args.gff, org_id, an_id, int(args.import_mode == 'add_only'),
                    int(args.import_mode == 'update'), int(args.import_mode == 'refresh'), int(args.import_mode == 'remove'),
                    transaction, target_org_id, args.target_type, int(args.target_create), args.start_line,
                    args.landmark_type, args.alt_id_attr, int(args.create_organism), args.re_mrna, args.re_protein]

        r = ti.jobs.addJob(job_name, 'tripal_feature', 'tripal_feature_load_gff3', job_args)
        print('Load GFF3 job scheduled with id %s' % r['job_id'])
