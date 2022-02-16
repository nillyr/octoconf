# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from icecream import ic
import xlsxwriter

from octoconf.ports import IReportGenerator
from octoconf.utils import global_values
from octoconf.utils.config import Config


class ReportGeneratorAdapter(IReportGenerator):
    """
    Generates a report in Excel format (xlsx).
    """

    _config = None

    def __init__(self) -> None:
        self._synthesis = dict()
        # There is no need to load the configuration.
        # This is done when the tool / unit test is launched.
        self._config = Config()

    def _get_category_format(self, workbook: xlsxwriter.workbook.Workbook):
        """
        Definition of the style to be applied.
        """
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": self._config.get_config("report_colors", "font_color"),
                "fg_color": self._config.get_config(
                    "report_colors", "category_foreground_color"
                ),
            }
        )

    def _get_checkpoint_format(self, workbook: xlsxwriter.workbook.Workbook):
        """
        Definition of the style to be applied.
        """
        return workbook.add_format(
            {
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": self._config.get_config("report_colors", "font_color"),
                "fg_color": self._config.get_config(
                    "report_colors", "checkpoint_foreground_color"
                ),
            }
        )

    def _get_severity_result_format(
        self, severity: str, workbook: xlsxwriter.workbook.Workbook
    ):
        """
        Definition of the style to be applied.
        """
        if severity == "info":
            font_color = self._config.get_config("severity_colors", "s_info")
        elif severity == "low":
            font_color = self._config.get_config("severity_colors", "s_low")
        elif severity == "medium":
            font_color = self._config.get_config("severity_colors", "s_medium")
        else:
            font_color = self._config.get_config("severity_colors", "s_high")

        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": font_color,
            }
        )

    def _get_check_format(self, workbook: xlsxwriter.workbook.Workbook):
        """
        Definition of the style to be applied.
        """
        return workbook.add_format(
            {
                "border": 1,
                "align": "left",
                "valign": "vcenter",
            }
        )

    def _get_success_result_format(self, workbook: xlsxwriter.workbook.Workbook):
        """
        Definition of the style to be applied.
        """
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": self._config.get_config("status_colors", "success"),
            }
        )

    def _get_failed_result_format(self, workbook: xlsxwriter.workbook.Workbook):
        """
        Definition of the style to be applied.
        """
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": self._config.get_config("status_colors", "failed"),
            }
        )

    def _get_uncertain_result_format(self, workbook: xlsxwriter.workbook.Workbook):
        """
        Definition of the style to be applied.
        """
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": self._config.get_config("status_colors", "to_be_defined"),
            }
        )

    def _write_results(self, workbook: xlsxwriter.workbook.Workbook, data: list):
        """
        Add the results obtained during the verification for each of the checks.
        """
        for category in data["categories"][0]:
            # It is not possible to use a worksheet's title > 31 chars, so we need to slice
            worksheet = workbook.add_worksheet(name=category["name"][0:31])
            worksheet.set_column("A:E", 20)
            worksheet.set_row(0, 25)
            worksheet.merge_range(
                "A1:E1", category["name"], self._get_category_format(workbook)
            )
            checkpoint_row = 2
            nb_success, nb_failed, nb_na = 0, 0, 0
            for checkpoint in category["checkpoints"]:
                worksheet.write(
                    f"A{checkpoint_row}",
                    global_values.localize.gettext("severity"),
                    self._get_checkpoint_format(workbook),
                )
                worksheet.merge_range(
                    f"B{checkpoint_row}:D{checkpoint_row}",
                    checkpoint["title"],
                    self._get_checkpoint_format(workbook),
                )
                worksheet.write(
                    f"E{checkpoint_row}",
                    global_values.localize.gettext("result"),
                    self._get_checkpoint_format(workbook),
                )
                check_row = checkpoint_row + 1
                for check in checkpoint["checks"]:
                    worksheet.write(
                        f"A{check_row}",
                        global_values.localize.gettext(check["severity"]),
                        self._get_severity_result_format(check["severity"], workbook),
                    )
                    worksheet.merge_range(
                        f"B{check_row}:D{check_row}",
                        check["title"],
                        self._get_check_format(workbook),
                    )
                    if "result" in check:
                        if check["result"] == True:
                            worksheet.write(
                                f"E{check_row}",
                                global_values.localize.gettext("success"),
                                self._get_success_result_format(workbook),
                            )
                            nb_success += 1
                        elif check["result"] == False:
                            worksheet.write(
                                f"E{check_row}",
                                global_values.localize.gettext("failed"),
                                self._get_failed_result_format(workbook),
                            )
                            nb_failed += 1
                        else:
                            worksheet.write(
                                f"E{check_row}",
                                global_values.localize.gettext("na"),
                                self._get_uncertain_result_format(workbook),
                            )
                            nb_na += 1
                        check_row += 1
                        checkpoint_row = check_row
                    else:
                        worksheet.write(
                            f"E{check_row}",
                            global_values.localize.gettext("na"),
                            self._get_uncertain_result_format(workbook),
                        )
                        nb_na += 1
                        check_row += 1
                        checkpoint_row = check_row

            self._synthesis[category["name"]] = {
                "SUCCESS": nb_success,
                "FAILED": nb_failed,
                "N/A": nb_na,
            }

    # fmt:off
    def _generate_synthesis(self,
                            workbook: xlsxwriter.workbook.Workbook,
                            worksheet: xlsxwriter.worksheet.Worksheet) -> int:
    #fmt:on
        """
        Resumes all the sheets (categories) of the excel file in order to present in the same sheet the synthesis of the results.
        """
        worksheet.set_column("A:G", 15)
        worksheet.set_row(0, 25)
        worksheet.merge_range("A1:G1", global_values.localize.gettext("summary"), self._get_category_format(workbook))
        worksheet.merge_range(
            "A2:C2", global_values.localize.gettext("categories"), self._get_checkpoint_format(workbook)
        )
        worksheet.write("D2", f"# {global_values.localize.gettext('success')}", self._get_checkpoint_format(workbook))
        worksheet.write("E2", f"# {global_values.localize.gettext('failed')}", self._get_checkpoint_format(workbook))
        worksheet.write("F2", f"# {global_values.localize.gettext('na')}", self._get_checkpoint_format(workbook))
        worksheet.write("G2", f"% {global_values.localize.gettext('percent')}", self._get_checkpoint_format(workbook))

        row = 2
        for key, value in self._synthesis.items():
            row += 1
            ic(key, value["SUCCESS"], value["FAILED"], value["N/A"])
            worksheet.merge_range(
                f"A{row}:C{row}",
                key,
                self._get_check_format(workbook),
            )
            worksheet.write(
                f"D{row}",
                value["SUCCESS"],
                self._get_check_format(workbook),
            )
            worksheet.write(
                f"E{row}",
                value["FAILED"],
                self._get_check_format(workbook),
            )
            worksheet.write(
                f"F{row}",
                value["N/A"],
                self._get_check_format(workbook),
            )
            try:
                worksheet.write(
                    f"G{row}",
                    (value["SUCCESS"] * 100)
                    / (value["SUCCESS"] + value["FAILED"] + value["N/A"]),
                    self._get_check_format(workbook),
                )
            except ZeroDivisionError:
                worksheet.write(
                    f"G{row}",
                    0,
                    self._get_check_format(workbook),
                )
        return row

    #fmt:off
    def _generate_charts(self,
                            workbook: xlsxwriter.workbook.Workbook,
                            worksheet: xlsxwriter.worksheet.Worksheet,
                            last_row: int):
    #fmt:on
        """
        A picture is worth a thousand words, and this method generates charts indicating the coverage level of security configurations.
        """
        # Radar
        radar_chart = workbook.add_chart({"type": "radar", "subtype": "filled"})
        radar_chart.set_title({"name": global_values.localize.gettext("cov_summary")})
        radar_chart.add_series(
            {
                "name": f"={global_values.localize.gettext('summary')}!$G$2",
                "categories": f"={global_values.localize.gettext('summary')}!$A$3:$A${last_row}",
                "values": f"={global_values.localize.gettext('summary')}!$G$3:$G${last_row}",
                "fill": {"color": "green"},
            }
        )
        worksheet.insert_chart("J1", radar_chart)

        # Column
        column_chart = workbook.add_chart({"type": "column"})
        column_chart.set_title({"name": global_values.localize.gettext("cov_summary")})
        column_chart.set_x_axis({"name": global_values.localize.gettext("categories")})
        column_chart.set_y_axis({"name": global_values.localize.gettext("nb_checks")})
        column_chart.add_series(
            {
                "name": f"={global_values.localize.gettext('summary')}!$D$2",
                "categories": f"={global_values.localize.gettext('summary')}!$A$3:$A${last_row}",
                "values": f"={global_values.localize.gettext('summary')}!$D$3:$D${last_row}",
                "fill": {"color": "green"},
            }
        )
        column_chart.add_series(
            {
                "name": f"={global_values.localize.gettext('summary')}!$E$2",
                "categories": f"={global_values.localize.gettext('summary')}!$A$3:$A${last_row}",
                "values": f"={global_values.localize.gettext('summary')}!$E$3:$E${last_row}",
                "fill": {"color": "red"},
            }
        )
        column_chart.add_series(
            {
                "name": f"={global_values.localize.gettext('summary')}!$F$2",
                "categories": f"={global_values.localize.gettext('summary')}!$A$3:$A${last_row}",
                "values": f"={global_values.localize.gettext('summary')}!$F$3:$F${last_row}",
                "fill": {"color": "blue"},
            }
        )
        column_chart.set_table({"show_keys": True})
        column_chart.set_legend({"position": "none"})
        worksheet.insert_chart(f"A{last_row + 5}", column_chart)

    def generate_report(self, data: list, filename: str):
        """
        Conducts the various methods of the class allowing the generation of the report.
        """
        workbook = xlsxwriter.Workbook(filename + ".xlsx")
        worksheet = workbook.add_worksheet(name=global_values.localize.gettext("summary"))
        self._write_results(workbook, data)
        last_row = self._generate_synthesis(workbook, worksheet)
        self._generate_charts(workbook, worksheet, last_row)
        workbook.close()
