#!/usr/bin/env python

import argparse
from icecream import ic
import os
import sys

from adapters import *
from models import *
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

  p.add_argument("--audit", metavar="CHECKLIST", type=str, help=
  "run an audit on the current system using a checklist")
  p.add_argument("--analyze", nargs=2, metavar=("ARCHIVE", "CHECKLIST"), 
  type=str, help="run an analysis on an archive (zip) containing all the configurations based on a checklist")
  p.add_argument("--regen-report", metavar="JSON", type=str, help=
  "regenerate a report based on a JSON output file provided by the other options")

  if len(sys.argv) == 1:
    p.print_help(file=sys.stderr)
    sys.exit(1)
  return p.parse_args()

def main():
  args = parse_args()
  if args.version:
    print("{} {}".format(
      os.path.splitext(os.path.basename(__file__))[0], const.VERSION))
    return 0
  if args.debug:
    debug.set_debug(True)
  if args.audit:
    checklist = ChecklistAdapter.checklist_parser(args.audit)
    ic('Received checklist:', checklist)
    return 0
  if args.regen_report:
    ic("TODO")
    return 0
  if args.analyze:
    ic("TODO")
    return 0

  return 0

if __name__ == "__main__":
  sys.exit(main())
