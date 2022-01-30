# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

#!/usr/bin/env python
# coding: utf-8

import argparse
from pathlib import Path
import sys

import inject

sys.path.append("../octoreconf/")
from octoreconf.adapters import (
    ArchiveAdapter,
    CheckerAdapter,
    ChecklistAdapter,
    CommandRunnerFactory,
    LanguageFactory,
)
from octoreconf.components.report_generators.xlsx_report_generator import XlsxGenerator
from octoreconf.components.translators.deepl_translator.deepl_translator import DeepL
from octoreconf.interactors import *
from octoreconf.ports import (
    IArchive,
    IChecker,
    IChecklist,
    ICommandRunnerFactory,
    ILanguageFactory,
    IReportGenerator,
    ITranslator,
)
from octoreconf.utils import *
from octoreconf.__init__ import __version__


def checklist_to_path(func):
    """
    Retrieves the path of the checklist requested by the user when it is a checklist present in the submodule.
    """

    def inner(*args, **kwargs):
        try:
            if not Path(args[0].checklist).exists():
                args[0].checklist = checklist_loader.get_checklist_path(
                    args[0].checklist
                )
            else:
                pass
        except:
            pass
        return func(*args, **kwargs)

    return inner


def default_parse_args(args):
    if args.version:
        print(f"octoreconf {__version__}")
    sys.exit(0)


@checklist_to_path
def parse_analyze_args(args):
    if args.debug:
        debug.set_debug(True)

    global_values.set_localize(args.language)
    print("[*] Launching the archive analysis...")
    uc = CheckArchiveInteractor()
    return uc.execute(args.checklist, args.archive)


@checklist_to_path
def parse_audit_args(args):
    if args.debug:
        debug.set_debug(True)

    global_values.set_localize(args.language)
    print("[*] Launching the audit...")
    uc = ChecksRunnerInteractor()
    return uc.execute(args.checklist, args.output)


@checklist_to_path
def parse_checklist_args(args) -> int:
    """
    Distinguishing arguments:
      - Generate: platform
      - Translate: target_lang
      - Export: checklist
      - List: category (can be none -> default behavior)
    """
    if args.debug:
        debug.set_debug(True)

    _ = vars(args)
    if _.get("platform"):
        # generate command
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
        return 0
    elif _.get("target_lang"):
        # translate command
        opts = {
            "checklist": args.checklist,
            "output": args.output,
            "source_lang": args.source_lang,
            "target_lang": args.target_lang,
        }
        print("[*] Launching the checklist translation...")
        translator = ChecklistTranslatorInteractor()
        translator.execute(opts)
        print("[+] Done")
        return 0
    elif _.get("checklist"):
        # export
        print("[*] Launching the checklist exportation...")
        status = ChecklistExporter.export(args.checklist, args.output)
        if status == 0:
            print(f"[+] The checklist has been exported here: {args.output}")
            print("[+] Done")
        else:
            print("[x] Error: something went wrong")
        return status
    else:
        # list by default
        category = None
        try:
            category = args.category
        except:
            pass

        checklists = checklist_loader.get_checklists(category)
        print("Available checklists:")
        for checklist_category in checklists.keys():
            for checklist_name in checklists[checklist_category]:
                print(f"\t{checklist_category}/{checklist_name}")
    return 0


def parse_report_args(args):
    if args.debug:
        debug.set_debug(True)

    global_values.set_localize(args.language)
    uc = ReportGeneratorInteractor()
    return uc.execute(args.input, is_file=True)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        ,'""`.       octoreconf {}
       / _  _ \\
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\\
     (( ((  )) ))    /** Nicolas GRELLETY ( ngy.cs@protonmail.com ) **/
   hh `\ `)(' /'
  """.format(
            __version__
        ),
    )

    p.add_argument(
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

    ## Checklist ##
    checklist_parser = cmd.add_parser(
        name="checklist", help="performs the interaction with the checklists"
    )
    checklist_parser.set_defaults(func=parse_checklist_args)
    checklists_commands = checklist_parser.add_subparsers(title="Commands")

    export_parser = checklists_commands.add_parser(
        name="export",
        help="performs a checklist export",
    )
    export_parser.add_argument(
        "-c",
        "--checklist",
        required=True,
        help="checklist to be exported",
    )
    export_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="output file to write results",
    )

    gen_script_parser = checklists_commands.add_parser(
        name="generate",
        help="performs the generation of collection scripts based on a checklist",
    )
    gen_script_parser.add_argument(
        "-c",
        "--checklist",
        required=True,
        help="checklist",
    )
    gen_script_parser.add_argument(
        "-l",
        "--language",
        choices=("bash", "batch", "powershell"),
        default="bash",
        required=True,
        help="script language",
    )
    gen_script_parser.add_argument(
        "-p",
        "--platform",
        required=True,
        choices=("mac", "linux", "windows"),
        help="targeted platform",
    )
    gen_script_parser.add_argument(
        "-o", "--output", required=True, help="output file to write results"
    )

    list_parser = checklists_commands.add_parser(
        name="list", help="performs a listing of the checklists (default behavior)"
    )
    list_parser.add_argument(
        "-c",
        "--category",
        required=False,
        help="Filter checklists on a given category",
    )

    translate_parser = checklists_commands.add_parser(
        name="translate", help="performs checklist translation"
    )
    translate_parser.add_argument(
        "-c",
        "--checklist",
        required=True,
        help="checklist",
    )
    translate_parser.add_argument(
        "-o", "--output", required=True, help="output file to write results"
    )
    translate_parser.add_argument(
        "-s",
        "--source_lang",
        required=False,
        default="EN",
        help="iso code of the source language (ex.: FR, EN, RU, etc.)",
    )
    translate_parser.add_argument(
        "-t",
        "--target_lang",
        required=True,
        help="iso code of the target language (ex.: FR, EN, RU, etc.)",
    )

    ## Report ##
    report_parser = cmd.add_parser(
        name="report", help="performs the generation of audit reports"
    )
    report_parser.set_defaults(func=parse_report_args)

    report_parser.add_argument("-i", "--input", required=True, help="JSON results file")
    report_parser.add_argument(
        "-l", "--language", default="EN", help="EN/FR (default=EN)"
    )

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
    binder.bind(ICommandRunnerFactory, CommandRunnerFactory())
    binder.bind(ILanguageFactory, LanguageFactory())
    binder.bind(IReportGenerator, XlsxGenerator())
    binder.bind(ITranslator, DeepL())


def cli():
    try:
        # Configuration steps
        inject.configure(dependency_injection_configuration)
        global checklist_loader
        checklist_loader = ChecklistsLoader()
        checklist_loader()

        sys.exit(parse_args())
    except Exception as _err:
        print(f"{_err}", file=sys.stderr)


if __name__ == "__main__":
    cli()
