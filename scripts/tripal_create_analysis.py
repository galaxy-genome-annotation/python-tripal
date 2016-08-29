#!/usr/bin/env python
import os
import json
import argparse
from tripal import TripalAuth, TripalAnalysis, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates an analysis into Tripal')
    TripalAuth(parser)
    TripalAnalysis(parser)

    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    params = ti.analysis.getBasePayload(args)

    params.update({
        'type': 'chado_analysis',
    })

    res = ti.analysis.addAnalysis(params)

    print "New analysis created with ID: %s" % res['nid']
