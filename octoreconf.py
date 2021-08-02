#!/usr/bin/env python

import argparse
import config.constants as const
from icecream import ic
import os
import sys
from utils.utils import Debug

#### Global variables ####
debug = Debug()


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
  const.get_version()))

  p.add_argument("-v", "--version", default=False, 
  help="print version", action="store_true")
  p.add_argument("-d", "--debug", default=False, 
  help="debug output (verbose)", action="store_true")

  p.add_argument("--audit", metavar="CHECKLIST", type=str, help=
  "runs an audit on the current system using a checklist")
  p.add_argument("--regen-report", metavar="JSON", type=str, help=
  "regenerate a report based on a JSON output file provided by the 'audit' option")
  p.add_argument("--analyze", nargs=2, metavar=("CHECKLIST", "ARCHIVE"), 
  type=str, help="runs an analysis based on a checklist and an archive (zip) containing all the configurations")
  p.add_argument("--password", default=None, type=str, 
  help="archive decryption password")

  if len(sys.argv) == 1:
    p.print_help(file=sys.stderr)
    sys.exit(1)
  return p.parse_args()

def main():
  args = parse_args()
  if args.version:
    print("{} {}".format(
      os.path.splitext(os.path.basename(__file__))[0], const.get_version()))
    return 0
  if args.debug:
    debug.set_debug(True)
  if args.audit:
    ic("TODO")
    return 0
  if args.regen_report:
    ic("TODO")
    return 0
  if args.analyze:
    ic("TODO")
    if args.password:
      ic("TODO")
    return 0

  return 0

if __name__ == "__main__":
  sys.exit(main())
