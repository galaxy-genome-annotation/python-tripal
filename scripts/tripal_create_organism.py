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

    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    params = {
        'type': 'chado_organism',
        'genus': args.genus,
        'species': args.species,
        'abbreviation': args.abbr,
        'common_name': args.common,
        'description': args.description,
    }

    res = ti.organism.addOrganism(params)

    print "New organism created with ID: %s" % res['nid']
