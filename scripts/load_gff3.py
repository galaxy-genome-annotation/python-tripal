#!/usr/bin/env python
import os
import json
import argparse
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads a GFF3 file into Tripal')
    TripalAuth(parser)
    parser.add_argument('gff', help='Path to the GFF3 file to load')
    parser.add_argument('--job-name', help='Name of the job (default=\'Import GFF3 file: <gff3_file_name>\')')
    parser.add_argument('--organism-id', type=int, required=True, help='Organism ID')
    parser.add_argument('--analysis-id', type=int, required=True, help='Analysis ID')
    parser.add_argument('--import-mode', choices=['add_only', 'update', 'refresh', 'remove'], default='update', help='Import mode, default=update (add_only=existing features won\'t be touched, update=existing features will be updated and obsolete attributes kept, refresh=existing features will be updated and obsolete attributes removed, remove=features present in the db and in the GFF3 file will be reomved)')
    parser.add_argument('--target-organism-id', type=int, help='In case of Target attribute in the GFF3, choose the organism to which target sequences belong. Select this only if target sequences belong to a different organism than the one specified with --organism-id. And only choose an organism here if all of the target sequences belong to the same species. If the targets in the GFF file belong to multiple different species then the organism must be specified using the \'target_organism=genus:species\' attribute in the GFF file.')
    parser.add_argument('--target-type', help='In case of Target attribute in the GFF3, if the unique name for a target sequence is not unique (e.g. a protein and an mRNA have the same name) then you must specify the type for all targets in the GFF file. If the targets are of different types then the type must be specified using the \'target_type=type\' attribute in the GFF file. This must be a valid Sequence Ontology (SO) term.')
    parser.add_argument('--target-create', action='store_true', help='In case of Target attribute in the GFF3, if the target feature cannot be found, create one using the organism and type specified above, or using the \'target_organism\' and \'target_type\' fields specified in the GFF file. Values specified in the GFF file take precedence over those specified above.')
    parser.add_argument('--start-line', type=int, help='The line in the GFF file where importing should start')
    parser.add_argument('--landmark-type', help='A Sequence Ontology type for the landmark sequences in the GFF fie (e.g. \'chromosome\'). If the GFF file contains a \'##sequence-region\' line that describes the landmark sequences to which all others are aligned and a type is provided here then the features will be created if they do not already exist. If they do exist then this field is not used')
    parser.add_argument('--alt-id-attr', help='Sometimes lines in the GFF file are missing the required ID attribute that specifies the unique name of the feature, but there may be another attribute that can uniquely identify the feature. If so, you may specify the name of the attribute to use for the name.')
    parser.add_argument('--re-mrna', help='Regular expression for the mRNA name')
    parser.add_argument('--re-protein', help='Replacement string for the protein name')
    parser.add_argument('--create-organism', action='store_true', help='The Tripal GFF loader supports the "organism" attribute. This allows features of a different organism to be aligned to the landmark sequence of another species. The format of the attribute is "organism=[genus]:[species]", where [genus] is the organism\'s genus and [species] is the species name. Check this box to automatically add the organism to the database if it does not already exists. Otherwise lines with an organism attribute where the organism is not present in the database will be skipped.')

    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    job_name = args.job_name
    if not job_name:
        job_name = 'Import GFF3 file: %s' % os.path.basename(args.gff)

    transaction = 1 # use transaction or not, no reason to disable this

    job_args = [args.gff, args.organism_id, args.analysis_id, int(args.import_mode == 'add_only'),
                int(args.import_mode == 'update'), int(args.import_mode == 'refresh'), int(args.import_mode == 'remove'),
                transaction, args.target_organism_id, args.target_type, int(args.target_create), args.start_line,
                args.landmark_type, args.alt_id_attr, args.re_mrna, args.re_protein, int(args.create_organism)]

    print json.dumps(ti.jobs.addJob(job_name, 'tripal_feature', 'tripal_feature_load_gff3', job_args), indent=2)
