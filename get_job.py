#!/usr/bin/env python
import json
import argparse
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get details about a specific Tripal job')
    TripalAuth(parser)
    parser.add_argument('job_id', type=int, help='ID of the job to retrieve')
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    print json.dumps(ti.jobs.getJob(args.job_id), indent=2)
