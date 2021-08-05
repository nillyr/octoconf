#!/usr/bin/env python

import argparse
from icecream import ic
import os
import sys
from utils import *

const.VERSION = "v1.0.0b"
const.COLORS = {
  'DARK_BLUE':'333E4E',
  'LIGHT_BLUE':'8496AF',
  'LIGT_GRAY': 'D9D9D9',
  'LIGHT_GREEN': '92D050',
  'LIGHT_ORANGE': 'F6C180',
  'LIGHT_YELLOW': 'FFFF66',
  'REGULAR_BLUE': '3891DE',
  'REGULAR_GREEN': '009644',
  'REGULAR_ORANGE': 'F1992D',
  'REGULAR_RED': 'C51718'
}

def default_parse_args(args):
  if args.version:
    print(os.path.splitext(os.path.basename(__file__))[0], 
  const.VERSION)
  sys.exit(0)

def parse_analyze_args(args):
  if args.debug:
    debug.set_debug(True)

  archive, checklist, output = (args.archive, args.checklist, args.output)
  ic(archive, checklist, output)
  #TODO

def parse_audit_args(args):
  if args.debug:
    debug.set_debug(True)

  checklist, output = (args.checklist, args.output)
  ic(checklist, output)
  #TODO

def parse_misc_args(args):
  if args.debug:
    debug.set_debug(True)
  
  if args.gen_collection_script:
    checklist, extension, output = (args.gen_collection_script, args.extension, args.output)
    ic(checklist, extension, output)
    #TODO
  if args.regen_report:
    results, output = (args.regen_report, args.output)
    ic(results, output)
    #TODO

def parse_args() -> argparse.Namespace:
  p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
  description='''
        ,'""`.       {} {}
       / _  _ \\ 
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\\
     (( ((  )) ))    /** Nicolas GRELLETY ( ngy.cs@protonmail.com ) **/
   hh `\ `)(' /'
  '''.format(os.path.splitext(os.path.basename(__file__))[0], 
  const.VERSION))

  p.add_argument("-v", "--version", default=False, 
  help="print version and exit", action="store_true")
  p.add_argument("-d", "--debug", default=False, 
  help="debug output (verbose)", action="store_true")

  p.set_defaults(func=default_parse_args)

  cmd = p.add_subparsers(help="Available Commands")

  analyze_parser = cmd.add_parser(name='analyze', help='performs an analysis on an archive based on a checklist')
  audit_parser = cmd.add_parser(name='audit', help='performs an audit of the host based on a checklist')
  misc_parser = cmd.add_parser(name='misc', help='miscellaneous commands')

  analyze_parser.set_defaults(func=parse_analyze_args)
  audit_parser.set_defaults(func=parse_audit_args)
  misc_parser.set_defaults(func=parse_misc_args)

  analyze_parser.add_argument('-a', '--archive', required=True, type=str, help="archive to use")
  analyze_parser.add_argument('-c', '--checklist', required=True, type=str, help="checklist to use")
  analyze_parser.add_argument("-o", "--output", help="output file to write results")

  audit_parser.add_argument("-c", "--checklist", required=True, help=
  "run an audit on the current system using a checklist")
  audit_parser.add_argument("-o", "--output", help="output file to write results")

  misc_parser.add_argument("--gen-collection-script", metavar="CHECKLIST", help="generate a collection script from the provided checklist")
  misc_parser.add_argument("--regen-report", metavar="JSON", type=str, help=
  "regenerate a report based on a JSON output file provided by the other options")
  misc_parser.add_argument("-e", "--extension", choices=['bat', 'ps1', 'sh'], help="output script extension")
  misc_parser.add_argument("-o", "--output", help="output file to write results")

  if len(sys.argv) == 1:
    p.print_help(file=sys.stderr)
    sys.exit(1)

  args = p.parse_args()
  return args.func(args)

if __name__ == "__main__":
  sys.exit(parse_args())
