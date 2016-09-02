#!/usr/bin/env python
import os
import json
import argparse
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates an organism into Tripal')
    TripalAuth(parser)
    parser.add_argument("--genus", required=True, help="The genus of the organism")
    parser.add_argument("--species", help="The species of the organism")
    parser.add_argument("--abbr", required=True, help="The abbreviation of the organism")
    parser.add_argument("--common", required=True, help="The common name of the organism")
    parser.add_argument("--description", help="The abbreviation of the organism")
    parser.add_argument("--infraspecific-rank", type=int, help="The type id of infraspecific name for any taxon below the rank of species (requires --infraspecific-name.") # TODO use readable names instead of id
    parser.add_argument("--infraspecific-name", help="The infraspecific name for this organism (requires --infraspecific-rank).")

    args = parser.parse_args()

    if (args.infraspecific_rank or args.infraspecific_name) and not (args.infraspecific_name and args.infraspecific_rank):
        raise Exception("You should specific both --infraspecific-rank and --infraspecific-name, or none of them.")

    ti = TripalInstance(args.tripal, args.username, args.password)

    params = {
        'type': 'chado_organism',
        'genus': args.genus,
        'species': args.species,
        'abbreviation': args.abbr,
        'common_name': args.common,
        'description': args.description,
        'type_id': 0,
        'infraspecific_name': '',
    }

    if args.infraspecific_rank:
        params['infraspecific_rank'] = args.infraspecific_rank
        params['infraspecific_name'] = args.infraspecific_name

    res = ti.organism.addOrganism(params)

    print "New organism created with Node ID: %s" % res['nid']
