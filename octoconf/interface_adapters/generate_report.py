# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import csv
import logging
from pathlib import Path
from typing import Any

from octoconf.entities.baseline import Baseline
from octoconf.interfaces.generate_report import IReportGenerator
import octoconf.utils.global_values as global_values
from octoconf.utils.logger import *
from octoconf.utils.timestamp import timestamp

is_submodule_imported: bool = False
try:
    from octoconf.interface_adapters.octowriter.scripts.generate_pdf import PDFGenerator
    from octoconf.interface_adapters.octowriter.scripts.generate_xls import XLSGenerator

    is_submodule_imported = True
except ImportError:
    pass

logger = logging.getLogger(__name__)


class ReportGeneratorInterfaceAdapter(IReportGenerator):
    def __init__(self) -> None:
        super().__init__()

    def generate_csv(self, filename: str, results: Baseline, output_dir: Path) -> None:
        logger.debug(
            f"Running CSV report generation with the following arg: filename = {filename}, results = {results}, output_dir = {output_dir}"
        )
        header_columns = [
            global_values.localize.gettext("category_reference"),
            global_values.localize.gettext("category_name"),
            global_values.localize.gettext("rule_reference"),
            global_values.localize.gettext("rule_name"),
            global_values.localize.gettext("rule_level"),
            global_values.localize.gettext("rule_severity"),
            global_values.localize.gettext("compliant"),
        ]

        with open(f"{output_dir / filename}.csv", mode="w") as compliance_report:
            csv_writer = csv.DictWriter(
                compliance_report,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                fieldnames=header_columns,
            )
            csv_writer.writeheader()

            for category in results.categories:
                for rule in category.rules:
                    csv_writer.writerow(
                        {
                            global_values.localize.gettext(
                                "category_reference"
                            ): category.category,
                            global_values.localize.gettext(
                                "category_name"
                            ): category.name,
                            global_values.localize.gettext("rule_reference"): rule.id,
                            global_values.localize.gettext("rule_name"): rule.title,
                            global_values.localize.gettext("rule_level"): rule.level,
                            global_values.localize.gettext(
                                "rule_severity"
                            ): rule.severity,
                            global_values.localize.gettext("compliant"): rule.compliant,
                        }
                    )

    def regenerate_report(self, input_file: Path, args: Any) -> int:
        logger.debug(
            f"Running reports re-generation with the following arg: input_file = {input_file}, args = {args}"
        )
        try:
            if not is_submodule_imported:
                logger.debug("Submodules are not imported")
                return 1

            filename = f"octoconf_compliance_report_{timestamp()}"

            output_directory = Path(args.outdir) if args.outdir else Path.cwd()
            output_directory.mkdir(parents=True, exist_ok=True)

            PDFGenerator().build_pdf(
                filename,
                output_directory,
                input_file.parent,
                header_file=input_file.name,
                template_name=args.template_name,
                pdf_theme=args.pdf_theme,
            )
            return 0
        except:
            logger.exception("Catch an exception in report generation")
            return 1

    def generate_report(self, results: Baseline, args: Any) -> int:
        logger.debug(
            f"Running reports generation with the following arg: results = {results}, args = {args}"
        )
        try:
            filename = f"octoconf_compliance_report_{timestamp()}"

            output_directory = Path(args.outdir) if args.outdir else Path.cwd()
            output_directory.mkdir(parents=True, exist_ok=True)

            self.generate_csv(filename, results, output_directory)

            if is_submodule_imported:
                ini_file = Path(args.ini) if args.ini else None

                XLSGenerator().generate_xls(
                    filename, results, output_directory, ini_file
                )
                PDFGenerator().generate_pdf(
                    filename,
                    results,
                    output_directory,
                    ini_file,
                    args.template_name,
                    args.pdf_theme,
                )
            return 0
        except:
            logger.exception("Catch an exception in report generation")
            return 1
