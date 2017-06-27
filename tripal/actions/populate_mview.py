#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance


class populate_mview(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Populate materialized views')
        TripalAuth(parser)
        parser.add_argument('--job-name', help='Name of the job (default=\'Populate materialized view\')')
        parser.add_argument('--mview', help='Materialized view name (omit to populate all)')
        parser.add_argument('--no-wait', action='store_true', help='Do not wait for job to complete')

        args = parser.parse_args(args)

        self.ti = TripalInstance(**vars(args))

        if args.mview:
            mview_id = self.ti.tripaldb.getMviewByName(args.mview)['mview_id']

            self.add_job(args.mview, mview_id, args.no_wait)
        else:
            mviews = self.ti.tripaldb.getMviews()

            for m_name in mviews:
                self.add_job(m_name, mviews[m_name])

    def add_job(self, mview, mview_id, no_wait=False, job_name=None):
        if not job_name:
            job_name = 'Populate materialized views \'%s\'' % mview

        job_args = OrderedDict()
        job_args[0] = mview_id

        r = self.ti.jobs.addJob(job_name, 'tripal_core', 'tripal_populate_mview', job_args)
        print('Populate materialized view job scheduled with id %s' % r['job_id'])

        if not no_wait:
            run_res = self.ti.jobs.runJobs()
            self.ti.jobs.wait(r['job_id'])
            with open(run_res['stdout'], 'r') as fin:
                print(fin.read())
            with open(run_res['stderr'], 'r') as fin:
                print(fin.read(), file=sys.stderr)
