#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import os
import sys

from icecream import ic
import inject

from adapters import ArchiveAdapter, CheckerAdapter, ChecklistAdapter, LanguageFactory
from components.json_encoders.checkresult import CheckResultJsonEncoder
from components.report_generators import *
from interactors import *
from ports import IArchive, IChecker, IChecklist, ILanguageFactory
from utils import *


const.VERSION = "v1.2.6b"


def default_parse_args(args):
    if args.version:
        print(os.path.splitext(os.path.basename(__file__))[0], const.VERSION)
    sys.exit(0)


def parse_analyze_args(args):
    if args.debug:
        debug.set_debug(True)

    global_values.set_localize(args.language)
    print("[*] Launching the archive analysis...")
    uc = CheckArchiveInteractor()
    return uc.execute(args.checklist, args.archive)


def parse_audit_args(args):
    if args.debug:
        debug.set_debug(True)

    global_values.set_localize(args.language)
    print("[*] Launching the audit...")
    uc = ChecksRunnerInteractor()
    return uc.execute(args.checklist, args.output)


def parse_misc_args(args):
    if args.debug:
        debug.set_debug(True)

    _ = vars(args)
    # gen-report
    if _.get("input"):
        global_values.set_localize(args.language)
        uc = ReportGeneratorInteractor()
        return uc.execute(args.input, is_file=True)
    # gen-script
    if _.get("checklist"):
        opts = {
            "checklist": args.checklist,
            "output": args.output,
            "language": args.language,
            "platform": args.platform,
        }
        print("[*] Launching the script generation...")
        uc = CollectionScriptRetrievalInteractor()
        uc.execute(opts)
        print(f"[+] The generated script has been put here: {args.output}")
        print("[+] Done")
        return


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
    analyze_parser.add_argument(
        "-l", "--language", default="EN", help="EN/FR (default=EN)"
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
    audit_parser.add_argument(
        "-l", "--language", default="EN", help="EN/FR (default=EN)"
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
    csr_parser.add_argument(
        "-o", "--output", required=True, help="output file to write results"
    )

    # Report Generator
    rgr_parser = misc_cmd.add_parser(name="gen-report")
    rgr_parser.add_argument("-i", "--input", required=True, help="JSON results file")
    rgr_parser.add_argument("-l", "--language", default="EN", help="EN/FR (default=EN)")

    if len(sys.argv) == 1:
        p.print_help(file=sys.stderr)
        sys.exit(1)

    args = p.parse_args()
    return args.func(args)


def dependency_injection_configuration(binder):
    """
    Configuration of the dependency injection allowing not to be linked to a concrete implementation.
    """
    binder.bind(IArchive, ArchiveAdapter())
    binder.bind(IChecker, CheckerAdapter())
    binder.bind(IChecklist, ChecklistAdapter())
    binder.bind(ILanguageFactory, LanguageFactory())
    binder.bind(IReportGenerator, XlsxGenerator())


if __name__ == "__main__":
    inject.configure(dependency_injection_configuration)
    sys.exit(parse_args())
