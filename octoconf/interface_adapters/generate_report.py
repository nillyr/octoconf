# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import csv
import logging
from pathlib import Path
import shutil
from typing import Any
import zipfile

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
                theme_dir=args.theme_dir,
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
                    args.theme_dir,
                    args.pdf_theme,
                )
            return 0
        except:
            logger.exception("Catch an exception in report generation")
            return 1

    def list_available_templates(self) -> list:
        base_dir = Path(__file__).resolve().parent
        template_dir = base_dir / "octowriter" / "template"

        available_templates = []
        allowed_extensions = { ".yaml", ".yml" }

        for _, file in enumerate(template_dir.glob(r"**/*")):
            if not file.suffix in allowed_extensions:
                continue

            # We only need the pdf themes in <theme_dir> / resources / themes
            if not "themes" in str(file.parent):
                continue

            try:
                logger.debug(f"Found pdf-theme candidate: '{file}'")
            
                theme_dir = file.parents[2].stem
                theme = file.name

                if theme_dir == "default":
                    available_templates.append(
                        {
                            "theme_dir": theme_dir,
                            "theme": theme,
                            "path": file,
                            "source": "Built-in"
                        }
                    )
                else:
                    available_templates.append(
                        {
                            "theme_dir": theme_dir,
                            "theme": theme,
                            "path": file,
                            "source": "Custom"
                        }
                    )

            except:
                logger.exception(
                    f"Something went wrong when listing available templates for file '{file}'"
                )
                continue

        return available_templates

    def export_custom_templates(self) -> str:
        try:
            archive_name = Path.cwd() / f"octoconf_templates_export_{timestamp()}"
            root_dir = Path(__file__).resolve().parent / "octowriter" / "template"
            base_dir = "custom"

            return shutil.make_archive(
                archive_name, "zip", root_dir=str(root_dir), base_dir=base_dir
            )
        except:
            logger.exception("Unable to export custom templates")
            return None

    def import_custom_templates_from_archive(self, archive: str, action: str) -> Path:
        logger.info(
            f"Importing custom templates from '{archive}' with action '{action}'"
        )
        extract_dir = Path(__file__).resolve().parent / "octowriter" / "template"
        custom_templates_dir = extract_dir / "custom"
        custom_templates_tmp_dir = extract_dir / "custom_tmp"

        try:
            if custom_templates_tmp_dir.exists():
                shutil.rmtree(custom_templates_tmp_dir)
            logger.info("Saving the original state")
            shutil.copytree(custom_templates_dir, custom_templates_tmp_dir)
        except Exception as e:
            logger.exception(f"Catch exception {e}")
            return None

        # switch case 'match value: case value:' needs python 3.10
        # the tool must work with python 3.8
        if action.lower() == "merge":
            try:
                with zipfile.ZipFile(archive, "r") as zip_ref:
                    for zip_info in zip_ref.infolist():
                        file_path = Path(extract_dir) / zip_info.filename
                        if zip_info.is_dir():
                            file_path.mkdir(parents=True, exist_ok=True)
                        else:
                            with zip_ref.open(zip_info) as source, file_path.open(
                                "wb"
                            ) as target:
                                target.write(source.read())
            except:
                logger.exception("Unable to extract and merge custom templates")
                logger.info("Rollback the original state")
                if custom_templates_dir.exists():
                    shutil.rmtree(custom_templates_dir)

                shutil.move(custom_templates_tmp_dir, custom_templates_dir)
                return None
        else:
            try:
                if custom_templates_dir.exists():
                    shutil.rmtree(custom_templates_dir)

                with zipfile.ZipFile(archive, "r") as zip_ref:
                    if not "custom" in zip_ref.infolist()[0].filename.lower():
                        custom_templates_dir.mkdir(parents=True)
                        zip_ref.extractall(custom_templates_dir)
                    else:
                        zip_ref.extractall(extract_dir)
            except:
                logger.exception("Unable to extract and replace custom templates")
                logger.info("Rollback the original state")
                if custom_templates_dir.exists():
                    shutil.rmtree(custom_templates_dir)

                shutil.move(custom_templates_tmp_dir, custom_templates_dir)
                return None

        # Everything went well, the temporary directory can be removed
        try:
            logger.info("Removing the temporary directory")
            shutil.rmtree(custom_templates_tmp_dir)
        except:
            logger.exception("Unable to remove temporary directory")
        finally:
            return extract_dir / "custom"

