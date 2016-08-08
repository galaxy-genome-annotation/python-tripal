#!/usr/bin/env python
import json
import argparse
from tripal import TripalAuth, TripalInstance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List all Tripal jobs')
    TripalAuth(parser)
    args = parser.parse_args()

    ti = TripalInstance(args.tripal, args.username, args.password)

    print json.dumps(ti.jobs.getJobs(), indent=2)
