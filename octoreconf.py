#!/usr/bin/env python

from adapters import *
import argparse
from icecream import ic
from interactors import *
import os
import sys
from utils import *

const.VERSION = "v1.0.0b"
const.COLORS = {
    "DARK_BLUE": "333E4E",
    "LIGHT_BLUE": "8496AF",
    "LIGT_GRAY": "D9D9D9",
    "LIGHT_GREEN": "92D050",
    "LIGHT_ORANGE": "F6C180",
    "LIGHT_YELLOW": "FFFF66",
    "REGULAR_BLUE": "3891DE",
    "REGULAR_GREEN": "009644",
    "REGULAR_ORANGE": "F1992D",
    "REGULAR_RED": "C51718",
}


def default_parse_args(args):
    if args.version:
        print(os.path.splitext(os.path.basename(__file__))[0], const.VERSION)
    sys.exit(0)


def parse_analyze_args(args):
    if args.debug:
        debug.set_debug(True)

    archive, checklist = (args.archive, args.checklist)
    ic(archive, checklist)
    # TODO


def parse_audit_args(args):
    if args.debug:
        debug.set_debug(True)

    ic(args.checklist)
    adapter = ChecklistAdapter()
    uc_step1 = ChecksRunnerInteractor(adapter)
    results = uc_step1.execute(args.output, args.checklist)

    uc_step2 = CheckOutputInteractor(adapter)
    uc_step2.execute(args.output, args.checklist, results)


def parse_misc_args(args):
    if args.debug:
        debug.set_debug(True)

    _ = vars(args)
    # gen-script
    if _.get("checklist"):
        opts = {
            "checklist": args.checklist,
            "output": args.output,
            "language": args.language,
            "platform": args.platform,
        }
        ic(opts)
        adapter = ChecklistAdapter()
        uc = CollectionScriptRetrievalInteractor(adapter)
        return uc.execute(opts)
    # gen-report
    if _.get("input"):
        results, output = (args.input, args.output)
        ic(results, output)
        # TODO


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        ,'""`.       {} {}
       / _  _ \\
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\\
     (( ((  )) ))    /** Nicolas GRELLETY ( ngy.cs@protonmail.com ) **/
   hh `\ `)(' /'
  """.format(
            os.path.splitext(os.path.basename(__file__))[0], const.VERSION
        ),
    )

    p.add_argument(
        "-v",
        "--version",
        default=False,
        help="print version and exit",
        action="store_true",
    )
    p.add_argument(
        "-d",
        "--debug",
        default=False,
        help="debug output (verbose)",
        action="store_true",
    )
    p.set_defaults(func=default_parse_args)

    ### Commands ###
    cmd = p.add_subparsers(help="Available Commands")

    ## Analyze ##
    analyze_parser = cmd.add_parser(
        name="analyze", help="performs an analysis on an archive based on a checklist"
    )
    analyze_parser.set_defaults(func=parse_analyze_args)
    analyze_parser.add_argument(
        "-a", "--archive", required=True, type=str, help="archive to use"
    )
    analyze_parser.add_argument(
        "-c", "--checklist", required=True, type=str, help="checklist to use"
    )

    ## Audit ##
    audit_parser = cmd.add_parser(
        name="audit", help="performs an audit of the host based on a checklist"
    )
    audit_parser.set_defaults(func=parse_audit_args)
    audit_parser.add_argument(
        "-c",
        "--checklist",
        required=True,
        help="run an audit on the current system using a checklist",
    )
    audit_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="basedir output for collection commands",
    )

    ## MISC ##
    misc_parser = cmd.add_parser(name="misc", help="miscellaneous commands")
    misc_parser.set_defaults(func=parse_misc_args)
    misc_cmd = misc_parser.add_subparsers(title="Generators")

    # Collection Script Generator
    csr_parser = misc_cmd.add_parser(name="gen-script")
    csr_parser.add_argument(
        "-c",
        "--checklist",
        required=True,
        help="generate a collection script from the provided checklist",
    )
    csr_parser.add_argument(
        "-l",
        "--language",
        choices=("bash", "batch", "powershell"),
        default="bash",
        required=True,
        help="script language",
    )
    csr_parser.add_argument(
        "-p",
        "--platform",
        required=True,
        choices=("mac", "linux", "windows"),
        help="targeted platform",
    )
    csr_parser.add_argument("-o", "--output", help="output file to write results")

    # Report Generator
    rgr_parser = misc_cmd.add_parser(name="gen-report")
    rgr_parser.add_argument("-i", "--input", required=True, help="JSON results file")
    rgr_parser.add_argument("-o", "--output", help="output file to write results")

    if len(sys.argv) == 1:
        p.print_help(file=sys.stderr)
        sys.exit(1)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(parse_args())
