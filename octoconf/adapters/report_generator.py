# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import re

from typing import List
import xlsxwriter

from octoconf.ports import IReportGenerator
from octoconf.utils import global_values
import octoconf.utils.config as config


class ReportGeneratorAdapter(IReportGenerator):
    """
    Generates a report in Excel format (xlsx).
    """

    _config = None

    def __init__(self) -> None:
        self._synthesis: List = []

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
                "font_color": config.get_config("report_colors", "font_color"),
                "fg_color": config.get_config(
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
                "font_color": config.get_config("report_colors", "font_color"),
                "fg_color": config.get_config(
                    "report_colors", "checkpoint_foreground_color"
                ),
            }
        )

    def _get_level_format(self, level: str, workbook: xlsxwriter.workbook.Workbook):
        """
        Definition of the style to be applied.
        """
        if level == "high":
            font_color = config.get_config("level_colors", "lvl_high")
        elif level == "enhanced":
            font_color = config.get_config("level_colors", "lvl_enhanced")
        elif level == "intermediary":
            font_color = config.get_config("level_colors", "lvl_intermediary")
        else:
            font_color = config.get_config("level_colors", "lvl_minimal")

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
                "font_color": config.get_config("status_colors", "success"),
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
                "font_color": config.get_config("status_colors", "failed"),
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
                "font_color": config.get_config("status_colors", "to_be_defined"),
            }
        )

    def _define_conditional_formatting(self, workbook: xlsxwriter.workbook.Workbook, worksheet: xlsxwriter.workbook.Worksheet, range):
        worksheet.conditional_format(range,
            {'type': 'text',
                'criteria': 'containing',
                'value': global_values.localize.gettext("success"),
                'format': self._get_success_result_format(workbook)
            })
        worksheet.conditional_format(range,
            {'type': 'text',
                'criteria': 'containing',
                'value': global_values.localize.gettext("failed"),
                'format': self._get_failed_result_format(workbook)
            })
        worksheet.conditional_format(range,
            {'type': 'text',
                'criteria': 'containing',
                'value': global_values.localize.gettext("na"),
                'format': self._get_uncertain_result_format(workbook)
            })

    def _write_results(self, workbook: xlsxwriter.workbook.Workbook, data: list):
        """
        Add the results obtained during the verification for each of the checks.
        """
        for category in data["categories"][0]:
            # It is not possible to use a worksheet's title > 31 chars, so we need to slice
            regex = r"(</?x>)|[^a-zàâçéèêëîïôûù0-9\s\-]"
            category_name = re.sub(
                regex,
                "",
                category["name"][0:31],
                0,
                re.IGNORECASE,
            )
            worksheet = workbook.add_worksheet(name=category_name)
            worksheet.set_column("A:E", 20)
            worksheet.set_row(0, 25)
            worksheet.merge_range(
                "A1:E1", category["name"], self._get_category_format(workbook)
            )
            checkpoint_row = 2
            range = xlsxwriter.utility.xl_range(0, 4, 1048575, 4)
            self._define_conditional_formatting(workbook, worksheet, range)
            for checkpoint in category["checkpoints"]:
                worksheet.write(
                    f"A{checkpoint_row}",
                    global_values.localize.gettext("level"),
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
                    # Set data validation on result's cell
                    worksheet.data_validation(f"E{check_row}", {'validate': 'list',
                                  'source': [global_values.localize.gettext("success"), global_values.localize.gettext("failed"), global_values.localize.gettext("na")]})

                    worksheet.write(
                        f"A{check_row}",
                        global_values.localize.gettext(check["level"]),
                        self._get_level_format(check["level"], workbook),
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
                        elif check["result"] == False:
                            worksheet.write(
                                f"E{check_row}",
                                global_values.localize.gettext("failed"),
                                self._get_failed_result_format(workbook),
                            )
                        else:
                            worksheet.write(
                                f"E{check_row}",
                                global_values.localize.gettext("na"),
                                self._get_uncertain_result_format(workbook),
                            )
                        check_row += 1
                        checkpoint_row = check_row
                    else:
                        worksheet.write(
                            f"E{check_row}",
                            global_values.localize.gettext("na"),
                            self._get_uncertain_result_format(workbook),
                        )
                        check_row += 1
                        checkpoint_row = check_row

            self._synthesis.append(category_name)

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
        for category in self._synthesis:
            row += 1
            # A - C
            worksheet.merge_range(
                xlsxwriter.utility.xl_range(row - 1, 0, row - 1, 2),
                category,
                self._get_check_format(workbook),
            )
            # range = the col with the success/failed/na status (E) for each category
            range = f"'{category}'!{xlsxwriter.utility.xl_range(0, 4, 1048575, 4)}"
            criteria = '"'+global_values.localize.gettext('success')+'"'
            worksheet.write_formula(
                xlsxwriter.utility.xl_rowcol_to_cell(row - 1, 3),
                '=COUNTIF(%s,%s)' % (range, criteria),
                self._get_check_format(workbook),
            )
            criteria = '"'+global_values.localize.gettext('failed')+'"'
            worksheet.write_formula(
                xlsxwriter.utility.xl_rowcol_to_cell(row - 1, 4),
                '=COUNTIF(%s,%s)' % (range, criteria),
                self._get_check_format(workbook),
            )
            criteria = '"'+global_values.localize.gettext('na')+'"'
            worksheet.write_formula(
                xlsxwriter.utility.xl_rowcol_to_cell(row - 1, 5),
                '=COUNTIF(%s,%s)' % (range, criteria),
                self._get_check_format(workbook),
            )
            # Success col = D => col 3
            numerator_range = xlsxwriter.utility.xl_rowcol_to_cell(row - 1, 3)
            # Success col = D => col 3; Failed col = E => col 4 => range 3-4
            # N/A status is out
            denominator_range = xlsxwriter.utility.xl_range(row - 1, 3, row - 1, 4)
            worksheet.write_formula(
                xlsxwriter.utility.xl_rowcol_to_cell(row - 1, 6),
                "=(%s*100/SUM(%s))" % (numerator_range, denominator_range),
                self._get_check_format(workbook),
            )
        return row

    #fmt:off
    def _generate_charts(self,
                            workbook: xlsxwriter.workbook.Workbook,
                            worksheet: xlsxwriter.worksheet.Worksheet,
                            worksheet_name: str,
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
                "name": f"={worksheet_name}!$G$2",
                "categories": f"={worksheet_name}!$A$3:$A${last_row}",
                "values": f"={worksheet_name}!$G$3:$G${last_row}",
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
                "name": f"={worksheet_name}!$D$2",
                "categories": f"={worksheet_name}!$A$3:$A${last_row}",
                "values": f"={worksheet_name}!$D$3:$D${last_row}",
                "fill": {"color": "green"},
            }
        )
        column_chart.add_series(
            {
                "name": f"={worksheet_name}!$E$2",
                "categories": f"={worksheet_name}!$A$3:$A${last_row}",
                "values": f"={worksheet_name}!$E$3:$E${last_row}",
                "fill": {"color": "red"},
            }
        )
        column_chart.add_series(
            {
                "name": f"={worksheet_name}!$F$2",
                "categories": f"={worksheet_name}!$A$3:$A${last_row}",
                "values": f"={worksheet_name}!$F$3:$F${last_row}",
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
        worksheet_name = global_values.localize.gettext("summary")
        worksheet = workbook.add_worksheet(name=worksheet_name)
        # Write all results (one sheet per category)
        self._write_results(workbook, data)
        # Create the synthesis
        last_row = self._generate_synthesis(workbook, worksheet)
        # Add charts to the synthesis
        self._generate_charts(workbook, worksheet, worksheet_name, last_row)
        # Close the document
        workbook.close()
