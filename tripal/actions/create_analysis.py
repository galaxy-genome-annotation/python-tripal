#!/usr/bin/env python
from __future__ import print_function
import argparse
from tripal import TripalAuth, TripalAnalysis, TripalInstance


class create_analysis(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Creates an analysis into Tripal')
        TripalAuth(parser)
        TripalAnalysis(parser)

        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        params = ti.analysis.getBasePayload(args)

        params.update({
            'type': 'chado_analysis',
        })

        res = ti.analysis.addAnalysis(params)

        print("New analysis created with Node ID: %s" % res['nid'])
