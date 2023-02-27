# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import csv

from octoconf.entities.baseline import Baseline
from octoconf.interfaces.generate_report import IReportGenerator
import octoconf.utils.global_values as global_values
from octoconf.utils.timestamp import timestamp

is_submodule_imported: bool = False
try:
    #import octoconf.interface_adapters.octowriter.scripts.generate_html as HTMLGenerator
    #import octoconf.interface_adapters.octowriter.scripts.generate_pdf as PDFGenerator
    from octoconf.interface_adapters.octowriter.scripts.generate_xls import XLSGenerator
    is_submodule_imported = True
except ImportError:
    pass


class ReportGeneratorInterfaceAdapter(IReportGenerator):
    def __init__(self) -> None:
        super().__init__()

    def generate_csv(self, filename: str, results: Baseline) -> None:
        header_columns = [
          global_values.localize.gettext("category_reference"),
          global_values.localize.gettext("category_name"),
          global_values.localize.gettext("rule_reference"),
          global_values.localize.gettext("rule_name"),
          global_values.localize.gettext("rule_level"),
          global_values.localize.gettext("rule_severity"),
          global_values.localize.gettext("compliant"),
        ]

        with open(f"{filename}.csv", mode="w") as compliance_report:
            csv_writer = csv.DictWriter(compliance_report, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=header_columns)
            csv_writer.writeheader()

            for category in results.categories:
                for rule in category.rules:
                    csv_writer.writerow({
                        global_values.localize.gettext("category_reference"): category.category,
                        global_values.localize.gettext("category_name"): category.name,
                        global_values.localize.gettext("rule_reference"): rule.id,
                        global_values.localize.gettext("rule_name"): rule.title,
                        global_values.localize.gettext("rule_level"): rule.level,
                        global_values.localize.gettext("rule_severity"): rule.severity,
                        global_values.localize.gettext("compliant"): rule.compliant,
                    })
        compliance_report.close()

    def regenerate_report(results: str) -> int:
        try:
            if not is_submodule_imported:
                return 1

            # HTMLGenerator().build(results)
            # PDFGenerator().build(results)
            return 0
        except:
            return 1

    def generate_report(self, results: Baseline) -> int:
        try:
            filename = f"octoconf_compliance_report_{timestamp()}"
            self.generate_csv(filename, results)

            if is_submodule_imported:
                #HTMLGenerator().generate_html(filename, results)
                #PDFGenerator().generate_pdf(filename, results)
                XLSGenerator().generate_xls(filename, results)

            return 0
        except:
            return 1
