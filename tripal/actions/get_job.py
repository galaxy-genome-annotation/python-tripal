#!/usr/bin/env python
import json
import argparse
from tripal import TripalAuth, TripalInstance

class get_job(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Get details about a specific Tripal job')
        TripalAuth(parser)
        parser.add_argument('-j', '--job_id', type=int, help='ID of the job to retrieve (omit this option to get all jobs)')
        args = parser.parse_args(args)

        ti = TripalInstance(**vars(args))

        if args.job_id:
            print json.dumps(ti.jobs.getJob(args.job_id), indent=2)
        else:
            print json.dumps(ti.jobs.getJobs(), indent=2)
