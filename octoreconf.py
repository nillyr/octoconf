#!/usr/bin/env python

import argparse
import hjson
from icecream import ic
import json
import os
import sys
from utils import *

from models import *

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
# Should be usefull (eventually) later on...
hex2rgb = lambda x: tuple(int(x[i:i+2], 16) for i in (0, 2, 4))

def parse_checklist(filename):
  with open(filename, 'r') as hjson_file:
    hson_checklist = hjson.loads(hjson_file.read())
    json_checklist = hjson.dumpsJSON(hson_checklist)
    checklist = json.loads(json_checklist)

  categories_list = []
  for item in checklist:
    categories_list = []
    for category in item['categories']:
      checkpoints_list = []
      for checkpoint in category['checkpoints']:
        checks_list = []
        for check in checkpoint['checks']:
          checks_list.append(Check(**check))
        checkpoint['checks'] = checks_list
        checkpoints_list.append(Checkpoint(**checkpoint))
      category['checkpoints'] = checkpoints_list
      categories_list.append(Category(**category))

  return categories_list

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
    checklist = parse_checklist(args.audit)
    ic('TODO usecase')
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
