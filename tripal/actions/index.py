#!/usr/bin/env python
import json
import argparse
from collections import OrderedDict
from tripal import TripalAuth, TripalInstance

class index(object):

    def run(self, args):
        parser = argparse.ArgumentParser(prog=('tripal %s' % self.__class__.__name__), description='Index data with elasticsearch')
        TripalAuth(parser)
        parser.add_argument('-t', '--table', default='index_website', help='Name of a specific table to index (default="index_website" to index all the tripal content)')
        parser.add_argument('-q', '--queues', type=int, default=10, help='Number of cron queues to use')
        parser.add_argument('-f', '--fields', nargs='*', default=[], help='List of column names to index (omit to index all columns)')
        parser.add_argument('-l', '--links', nargs='*', default=[], help='List of links to show to users, syntax: <column-where-to-show-the-link>|</your/url/[any-column-name]>')

        args = parser.parse_args(args)

        links = {}
        for l in args.links:
            ls = l.split('|', 1)
            if ls[0] not in args.fields:
                raise Exception("Cannot add a link to column '%s' because it is not indexed" % ls[0])
            links[ls[0]] = ls[1]

        ti = TripalInstance(**vars(args))

        res = ti.tripaldb.index(args.table, args.queues, args.fields, links)

        print 'Scheduled indexing with elastic search'
