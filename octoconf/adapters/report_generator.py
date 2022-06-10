# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import re

import xlsxwriter

from octoconf.ports import IReportGenerator
from octoconf.utils import global_values
from octoconf.utils import timestamp
import octoconf.utils.config as config


class ReportGeneratorAdapter(IReportGenerator):
    _formats: dict = {}
    _synthesis: dict = {}
    _filename = timestamp() + "_results"

    wb: xlsxwriter.workbook.Workbook = None

    def __init__(self) -> None:
        self.wb = xlsxwriter.Workbook(self._filename + ".xlsx")
        self._add_format("header", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("report_colors", "header_font_color"),
            "bg_color": config.get_config(
                "report_colors", "header_background_color"
        )})
        self._add_format("sub_header", {
            "bold": 0,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("report_colors", "header_font_color"),
            "bg_color": config.get_config(
                "report_colors", "sub_header_background_color"
        )})
        self._add_format("minimal", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("level_colors", "lvl_minimal"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("intermediary", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("level_colors", "lvl_intermediary"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("enhanced", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("level_colors", "lvl_enhanced"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("high", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("level_colors", "lvl_high"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("check", {
            "bold": 0,
            "border": 1,
            "align": "left",
            "valign": "vcenter",
            "font_color": config.get_config("report_colors", "default_font_color"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("success", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("status_colors", "success"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("failed", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("status_colors", "failed"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("na", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_color": config.get_config("status_colors", "to_be_defined"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("total", {
            "bold": 1,
            "border": 1,
            "align": "left",
            "valign": "vcenter",
            "font_color": config.get_config("report_colors", "default_font_color"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })

    def _add_format(self, name:str, values: dict) -> None:
        # fmt:off
        self._formats[name] = self.wb.add_format(
            {
                "bold": values["bold"],
                "border": values["border"],
                "align": values["align"],
                "valign": values["valign"],
                "font_color": values["font_color"],
                "bg_color": values["bg_color"]
            })
        # fmt:on

    def _get_format(self, name: str) -> xlsxwriter.workbook.Format:
        if name in self._formats:
            return self._formats.get(name)

    def _add_conditional_formatting(self, ws: xlsxwriter.workbook.Worksheet, range) -> None:
        # fmt:off
        ws.conditional_format(range, {
            'type': 'text',
            'criteria': 'containing',
            'value': global_values.localize.gettext("success"),
            'format': self._get_format("success")
        })
        ws.conditional_format(range, {
            'type': 'text',
            'criteria': 'containing',
            'value': global_values.localize.gettext("failed"),
            'format': self._get_format("failed")
        })
        ws.conditional_format(range, {
            'type': 'text',
            'criteria': 'containing',
            'value': global_values.localize.gettext("na"),
            'format': self._get_format("na")
        })
        # fmt:on

    def _write_checkpoints_results_on_worksheet(self, ws: xlsxwriter.workbook.Worksheet, checkpoints: list) -> dict:
        # fmt:off
        results_by_levels = {
            global_values.localize.gettext("minimal").lower(): { "success": 0, "failed": 0},
            global_values.localize.gettext("intermediary").lower(): { "success": 0, "failed": 0},
            global_values.localize.gettext("enhanced").lower(): { "success": 0, "failed": 0},
            global_values.localize.gettext("high").lower(): { "success": 0, "failed": 0}
        }
        # fmt:on
        checkpoint_row = 2
        for checkpoint in checkpoints:
            ws.write(
                f"A{checkpoint_row}",
                global_values.localize.gettext("level"),
                self._get_format("sub_header"),
            )
            ws.merge_range(
                f"B{checkpoint_row}:D{checkpoint_row}",
                checkpoint["title"],
                self._get_format("sub_header"),
            )
            ws.write(
                f"E{checkpoint_row}",
                global_values.localize.gettext("result"),
                self._get_format("sub_header"),
            )

            check_row = checkpoint_row + 1
            for check in checkpoint["checks"]:
                ws.data_validation(f"E{check_row}", {
                    'validate': 'list',
                    'source': [
                        global_values.localize.gettext("success"),
                        global_values.localize.gettext("failed"),
                        global_values.localize.gettext("na")
                    ]
                })

                ws.write(
                    f"A{check_row}",
                    global_values.localize.gettext(check["level"]),
                    self._get_format(check["level"])
                )
                ws.merge_range(
                    f"B{check_row}:D{check_row}",
                    check["title"],
                    self._get_format("check")
                )
                if "result" in check:
                    if check["result"] == True:
                        results_by_levels[check["level"]]["success"] = results_by_levels[check["level"]]["success"] + 1
                        key = "success"
                    else:
                        results_by_levels[check["level"]]["failed"] = results_by_levels[check["level"]]["failed"] + 1
                        key = "failed"

                    ws.write(
                        f"E{check_row}",
                        global_values.localize.gettext(key),
                        self._get_format(key)
                    )
                else:
                    ws.write(
                        f"E{check_row}",
                        global_values.localize.gettext("na"),
                        self._get_format("na")
                    )
                check_row += 1
                checkpoint_row = check_row

        return results_by_levels

    def _write_results(self, categories: list) -> None:
        for category in categories:
            # It is not possible to use a worksheet's title > 31 chars, so we need to slice
            regex = r"(</?x>)|[^a-zàâçéèêëîïôûù0-9\s\-]"
            category_name = re.sub(
                regex,
                "",
                category["name"][0:31],
                0,
                re.IGNORECASE,
            )
            ws = self.wb.add_worksheet(name=category_name)
            ws.set_column("A:E", 20)
            ws.set_row(0, 25)
            ws.merge_range(
                "A1:E1", category["name"], self._get_format("header")
            )
            # Column 'E'
            range = xlsxwriter.utility.xl_range(0, 4, 1048575, 4)
            self._add_conditional_formatting(ws, range)
            # Write results in the worksheet and get nb of success/failed for stacked chart
            self._synthesis[category["name"]] = self._write_checkpoints_results_on_worksheet(ws, category["checkpoints"])

    def _add_synthesis(self, ws: xlsxwriter.worksheet.Worksheet) -> int:
        """
        Resumes all the sheets (categories) of the excel file in order to present in the same sheet the synthesis of the results.
        """
        ws.set_column("A:K", 15)
        ws.set_row(0, 25)
        ws.merge_range("A1:K1", global_values.localize.gettext("summary"), self._get_format("header"))
        ws.merge_range(
            "A2:C3", global_values.localize.gettext("categories"), self._get_format("sub_header")
        )
        ws.merge_range(
            "D2:G2", global_values.localize.gettext("success"), self._get_format("sub_header")
        )
        ws.merge_range(
            "H2:K2", global_values.localize.gettext("failed"), self._get_format("sub_header")
        )
        ws.write("D3", global_values.localize.gettext("minimal"), self._get_format("sub_header"))
        ws.write("E3", global_values.localize.gettext("intermediary"), self._get_format("sub_header"))
        ws.write("F3", global_values.localize.gettext("enhanced"), self._get_format("sub_header"))
        ws.write("G3", global_values.localize.gettext("high"), self._get_format("sub_header"))
        ws.write("H3", global_values.localize.gettext("minimal"), self._get_format("sub_header"))
        ws.write("I3", global_values.localize.gettext("intermediary"), self._get_format("sub_header"))
        ws.write("J3", global_values.localize.gettext("enhanced"), self._get_format("sub_header"))
        ws.write("K3", global_values.localize.gettext("high"), self._get_format("sub_header"))

        row = 3
        for category in self._synthesis:
            row += 1
            # A = 0, B = 1, C =2, D = 3
            # E = 4, F = 5, G = 6, H = 7
            # I = 8, J = 9, K = 10
            ws.merge_range(
                xlsxwriter.utility.xl_range(row - 1, 0, row - 1, 2),
                category,
                self._get_format("check"),
            )

            lvl_range = f"'{category}'!{xlsxwriter.utility.xl_range(0, 0, 1048575, 0)}"
            results_range = f"'{category}'!{xlsxwriter.utility.xl_range(0, 4, 1048575, 4)}"

            levels = [
                f"{lvl_range};\"{global_values.localize.gettext('minimal')}\"",
                f"{lvl_range};\"{global_values.localize.gettext('intermediary')}\"",
                f"{lvl_range};\"{global_values.localize.gettext('enhanced')}\"",
                f"{lvl_range};\"{global_values.localize.gettext('high')}\""
            ]

            success = {f"{results_range};\"{global_values.localize.gettext('success')}\"": levels}
            failed = {f"{results_range};\"{global_values.localize.gettext('failed')}\"": levels}

            start, stop = (3, 7)
            for criteria in success:
                for col in range(start, stop):
                    ws.write_formula(
                        xlsxwriter.utility.xl_rowcol_to_cell(row - 1, col),
                        "=COUNTIFS(%s; %s)" % (success[criteria][col - start], criteria),
                        self._get_format("check"),
                    )
            start, stop = (stop, 11)
            for criteria in failed:
                for col in range(start, stop):
                    ws.write_formula(
                        xlsxwriter.utility.xl_rowcol_to_cell(row - 1, col),
                        "=COUNTIFS(%s; %s)" % (failed[criteria][col - start], criteria),
                        self._get_format("check"),
                    )

        # Get total values
        ws.merge_range(
                xlsxwriter.utility.xl_range(row, 0, row, 2),
                "Total",
                self._get_format("total"),
        )
        start_row = 3
        for col in range(start_row, stop):
            ws.write_formula(
                xlsxwriter.utility.xl_rowcol_to_cell(row, col),
                "=SUM(%s)" % (xlsxwriter.utility.xl_range(start_row, col, row - 1, col)),
                self._get_format("total"),
            )

        return row + 1

    #fmt:off
    def _add_charts(self,
        ws: xlsxwriter.worksheet.Worksheet,
        last_row: int) -> None:
    #fmt:on
        """
        A picture is worth a thousand words, and this method generates charts indicating the coverage level of security configurations.
        """
        ws_name = ws.get_name()
        staked_chart_by_lvl = self.wb.add_chart({'type': 'column', 'subtype': 'stacked'})
        staked_chart_by_lvl.set_title({'name': global_values.localize.gettext("compliance_chart_title")})
        staked_chart_by_lvl.set_x_axis({'name': global_values.localize.gettext("levels")})
        staked_chart_by_lvl.set_y_axis({'name': global_values.localize.gettext("nb_checks"), 'major_gridlines': {'visible': False}})

        staked_chart_by_lvl.add_series({
            "name":         f"={ws_name}!$D$2",
            "categories":   f"={ws_name}!$D$3:$G$3",
            "values":       f"={ws_name}!$D${last_row}:G${last_row}",
            "data_labels":  {"value": True},
            "fill":         {"color": "#"+config.get_config("status_colors", "success")},
            "gap":          20
        })

        staked_chart_by_lvl.add_series({
            "name":         f"={ws_name}!$H$2",
            "categories":   f"={ws_name}!$H$3:$K$3",
            "values":       f"={ws_name}!$H${last_row}:K${last_row}",
            "data_labels":  {"value": True},
            "fill":         {"color": "#"+config.get_config("status_colors", "failed")},
            "gap":          20
        })

        ws.insert_chart(f"A{last_row+5}", staked_chart_by_lvl)

    def generate_report(self, data: list) -> str:
        ws = self.wb.add_worksheet(name=global_values.localize.gettext("summary"))
        self._write_results(data["categories"][0])
        last_row = self._add_synthesis(ws)
        self._add_charts(ws, last_row)
        self.wb.close()
        self.wb = None
        return self._filename
