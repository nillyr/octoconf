# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

import inject

sys.path.append("../octoconf/")
from octoconf.__init__ import __version__
from octoconf.components.translators.deepl_translator.deepl_translator import DeepL
from octoconf.interfaces.archive import IArchive
from octoconf.interfaces.baseline import IBaseline
from octoconf.interfaces.checker import IChecker
from octoconf.interfaces.generate_report import IReportGenerator
from octoconf.interfaces.generate_script.language_abstract_factory import ILanguageFactory
from octoconf.interfaces.translator import ITranslator
from octoconf.interface_adapters.archive import ArchiveInterfaceAdapter
from octoconf.interface_adapters.baseline import BaselineInterfaceAdapter
from octoconf.interface_adapters.checker import CheckerInterfaceAdapter
from octoconf.interface_adapters.generate_report import ReportGeneratorInterfaceAdapter
from octoconf.interface_adapters.generate_script.language_factory import LanguageFactory
from octoconf.use_cases.baseline_translator import BaselineTranslatorUseCase
from octoconf.use_cases.check_archive import CheckArchiveUseCase
from octoconf.use_cases.check_output import CheckOutputUseCase
from octoconf.use_cases.generate_report import GenerateReportUseCase
from octoconf.use_cases.generate_script import GenerateScriptUseCase
import octoconf.utils.config as config
import octoconf.utils.debug as debug
import octoconf.utils.global_values as global_values


def print_status(status) -> int:
    if status == 0:
        print("[+] Done!")
        return status
    else:
        print(f"[x] Error! Something went wrong.", file=sys.stderr)
        return status

def default_parse_args(args):
    if args.version:
        print(f"octoconf {__version__}")
    sys.exit(0)


def parse_analyze_args(args):
    if args.debug:
        debug.set_debug(True)

    global_values.set_localize(args.language)
    print("[*] Launching the archive analyis...")
    results = CheckArchiveUseCase().execute(args.baseline, args.archive)
    results = CheckOutputUseCase().execute(results)
    status = GenerateReportUseCase().execute(results, args)
    return print_status(status)


def parse_baseline_args(args):
    """
    Distinguishing arguments:
      - Generate script: platform
      - Translate: target_lang
    """
    if args.debug:
        debug.set_debug(True)

    _ = vars(args)
    if _.get("platform"):
        # generate_script command
        opts = {
            "baseline": args.baseline,
            "output": args.output,
            "platform": args.platform,
            "utils": args.utils
        }
        print("[*] Launching the script generation...")
        status = GenerateScriptUseCase().execute(opts)
        return print_status(status)
    elif _.get("target_lang"):
        # translate command
        opts = {
            "baseline": args.baseline,
            "output_directory": args.output,
            "source_lang": args.source_lang,
            "target_lang": args.target_lang,
        }
        print("[*] Launching the translation of the baseline...")
        status = BaselineTranslatorUseCase().execute(opts)
        return print_status(status)
    else:
        raise NotImplementedError("[x] Error! No suitable use case found.")


def parse_report_args(args):
    if args.debug:
        debug.set_debug(True)

    global_values.set_localize(args.language)
    print("[*] Launching report generation...")
    status = GenerateReportUseCase().execute(args.input, args, recompile=True)
    return print_status(status)


def parse_config_args(args):
    if "value" in args:
        # Edit sub-command
        return config.set_configuration_parameter(args)
    else:
        # Print sub-command
        return print(config.get_running_configuration())


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        ,'""`.       octoconf {}
       / _  _ \\
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\\
     (( ((  )) ))    /** @nillyr **/
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
        name="analyze", help="performs an analysis on an archive based on a security baseline"
    )
    analyze_parser.set_defaults(func=parse_analyze_args)
    analyze_parser.add_argument(
        "-a", "--archive", required=True, type=str, help="archive to use"
    )
    analyze_parser.add_argument(
        "-b", "--baseline", required=True, type=str, help="security baseline to use"
    )
    analyze_parser.add_argument(
        "-l", "--language", default=config.get_config("MISC", "language"), help="EN/FR (default=%s)" % (config.get_config("MISC", "language"))
    )
    analyze_parser.add_argument(
        "-o", "--outdir", required=False, type=str, default=None, help="output directory"
    )
    analyze_parser.add_argument(
        "--ini", required=False, type=str, default=None, help="[required dependency: asciidoctor-pdf] path to the configuration file (.ini) containing the required information to initialize the report"
    )
    analyze_parser.add_argument(
        "--imagesdir", required=False, type=str, default=None, help="[required dependency: asciidoctor-pdf] path to the folder containing the images to be used when generating the report"
    )
    analyze_parser.add_argument(
        "--pdf-themesdir", required=False, type=str, default=None, help="[required dependency: asciidoctor-pdf] path to the folder containing the stylesheet and associated images to be used when generating the report "
    )
    analyze_parser.add_argument(
        "--pdf-theme", required=False, type=str, default="custom-theme.yml", help="[required dependency: asciidoctor-pdf] name of the stylesheet in the 'pdf-themesdir' folder to use when generating the report"
    )

    ## Baseline ##
    baseline_parser = cmd.add_parser(
        name="baseline", help="performs the interaction with the security baselines"
    )
    baseline_parser.set_defaults(func=parse_baseline_args)
    baselines_commands = baseline_parser.add_subparsers(title="Commands")

    gen_script_parser = baselines_commands.add_parser(
        name="generate_script",
        help="performs the generation of collection scripts based on a security baseline",
    )
    gen_script_parser.add_argument(
        "-b",
        "--baseline",
        required=True,
        help="security baseline to use",
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
    gen_script_parser.add_argument(
        "-u", "--utils", required=False, default=None, help="path to a file containing utils functions to be included in the generated script"
    )

    translate_parser = baselines_commands.add_parser(
        name="translate", help="performs security baseline translation"
    )
    translate_parser.add_argument(
        "-b",
        "--baseline",
        required=True,
        help="security baseline",
    )
    translate_parser.add_argument(
        "-o", "--output", required=True, help="output file to write results"
    )
    translate_parser.add_argument(
        "-s",
        "--source_lang",
        required=False,
        default="EN",
        help="iso code of the source language (ex.: FR, EN, etc.)",
    )
    translate_parser.add_argument(
        "-t",
        "--target_lang",
        required=True,
        help="iso code of the target language (ex.: FR, EN, etc.)",
    )

    ## Report ##
    report_parser = cmd.add_parser(
        name="report", help="performs the recompilation of the report in PDF format from an adoc file"
    )
    report_parser.set_defaults(func=parse_report_args)

    report_parser.add_argument("-i", "--input", required=True, help="Asciidoc (.adoc) report file")
    report_parser.add_argument(
        "-l", "--language", default=config.get_config("MISC", "language"), help="EN/FR (default=%s)" % (config.get_config("MISC", "language"))
    )
    report_parser.add_argument(
        "-o", "--outdir", required=False, type=str, default=None, help="output directory"
    )
    report_parser.add_argument(
        "--imagesdir", required=False, type=str, default=None, help="[required dependency: asciidoctor-pdf] path to the folder containing the images to be used when generating the report"
    )
    report_parser.add_argument(
        "--pdf-themesdir", required=False, type=str, default=None, help="[required dependency: asciidoctor-pdf] path to the folder containing the stylesheet and associated images to be used when generating the report "
    )
    report_parser.add_argument(
        "--pdf-theme", required=False, type=str, default="custom-theme.yml", help="[required dependency: asciidoctor-pdf] name of the stylesheet in the 'pdf-themesdir' folder to use when generating the report"
    )

    ## Config ##
    config_parser = cmd.add_parser(
        name="config", help="performs octoconf configuration management"
    )
    config_parser.set_defaults(func=parse_config_args)
    config_commands = config_parser.add_subparsers(title="Commands")

    _ = config_commands.add_parser(
        name="print",
        help="print the current configuration",
    )

    edit_parser = config_commands.add_parser(
        name="edit",
        help="edit octoconf configuration",
    )
    edit_parser.add_argument(
        "-s",
        "--section",
        required=True,
        help="configuration section to edit",
    )
    edit_parser.add_argument(
        "-o",
        "--option",
        required=True,
        help="configuration option to edit",
    )
    edit_parser.add_argument(
        "-v",
        "--value",
        required=True,
        help="value to assign to the option",
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
    binder.bind(IArchive, ArchiveInterfaceAdapter())
    binder.bind(IChecker, CheckerInterfaceAdapter())
    binder.bind(IBaseline, BaselineInterfaceAdapter())
    binder.bind(ILanguageFactory, LanguageFactory())
    binder.bind(IReportGenerator, ReportGeneratorInterfaceAdapter())
    binder.bind(ITranslator, DeepL())


def cli():
    try:
        # Configuration steps
        inject.configure(dependency_injection_configuration)

        sys.exit(parse_args())
    except Exception as _err:
        print(f"{_err}", file=sys.stderr)


if __name__ == "__main__":
    cli()
