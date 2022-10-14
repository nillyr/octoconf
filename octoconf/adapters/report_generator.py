# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import re

import xlsxwriter

from octoconf.ports import IReportGenerator
from octoconf.utils import global_values
from octoconf.utils import timestamp, today
import octoconf.utils.config as config
from octoconf.__init__ import __version__, __url__

class ReportGeneratorAdapter(IReportGenerator):
    _formats: dict = {}
    _filename = timestamp() + "_results"

    wb: xlsxwriter.workbook.Workbook = None

    def __init__(self) -> None:
        self.wb = xlsxwriter.Workbook(self._filename + ".xlsx")
        self._add_format("information_header", {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "font_size": 14,
            "font_color": config.get_config("report_colors", "header_font_color"),
            "bg_color": config.get_config(
                "report_colors", "header_background_color"
        )})
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
        self._add_format("bold", {
            "bold": 1,
            "border": 1,
            "align": "left",
            "valign": "vcenter",
            "font_color": config.get_config("report_colors", "default_font_color"),
            "bg_color": config.get_config("report_colors", "default_background_color")
        })
        self._add_format("regular", {
            "bold": 0,
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
            'value': global_values.localize.gettext("minimal"),
            'format': self._get_format("minimal")
        })
        ws.conditional_format(range, {
            'type': 'text',
            'criteria': 'containing',
            'value': global_values.localize.gettext("intermediary"),
            'format': self._get_format("intermediary")
        })
        ws.conditional_format(range, {
            'type': 'text',
            'criteria': 'containing',
            'value': global_values.localize.gettext("enhanced"),
            'format': self._get_format("enhanced")
        })
        ws.conditional_format(range, {
            'type': 'text',
            'criteria': 'containing',
            'value': global_values.localize.gettext("high"),
            'format': self._get_format("high")
        })
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

    def _write_checkpoints_results_on_worksheet(self, ws: xlsxwriter.workbook.Worksheet, checkpoints: list) -> None:
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
                ws.data_validation(f"A{check_row}", {
                    'validate': 'list',
                    'source': [
                        global_values.localize.gettext("minimal"),
                        global_values.localize.gettext("intermediary"),
                        global_values.localize.gettext("enhanced"),
                        global_values.localize.gettext("high"),
                    ]
                })
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
                    key = "success" if check["result"] == True else "failed"
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
            ws.hide_gridlines(2)
            ws.set_column("A:A", 15)
            ws.set_column("B:D", 35)
            ws.set_column("E:E", 15)
            ws.set_row(0, 25)
            ws.merge_range(
                "A1:E1", category["name"], self._get_format("header")
            )
            # Column 'A' (level)
            range_a = xlsxwriter.utility.xl_range(0, 0, 1048575, 0)
            self._add_conditional_formatting(ws, range_a)
            # Column 'E' (result)
            range_e = xlsxwriter.utility.xl_range(0, 4, 1048575, 4)
            self._add_conditional_formatting(ws, range_e)
            # Write results in the worksheet and get nb of success/failed for stacked chart
            self._write_checkpoints_results_on_worksheet(ws, category["checkpoints"])

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

        # Do not stick the chart on the far left
        ws.insert_chart(f"D{last_row+5}", staked_chart_by_lvl)

    def _add_synthesis_worksheet(self, categories: list) -> None:
        """
        Resumes all the sheets (categories) of the excel file in order to present in the same sheet the synthesis of the results.
        """
        ws = self.wb.add_worksheet(name=global_values.localize.gettext("summary"))

        ws.hide_gridlines(2)
        ws.set_column("A:K", 20)
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
        for category in categories:
            category = category["name"]
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
                self._get_format("bold"),
        )
        start_row = 3
        for col in range(start_row, stop):
            ws.write_formula(
                xlsxwriter.utility.xl_rowcol_to_cell(row, col),
                "=SUM(%s)" % (xlsxwriter.utility.xl_range(start_row, col, row - 1, col)),
                self._get_format("bold"),
            )

        self._add_charts(ws, row + 1)

    def _add_information_worksheet(self, checklist: str) -> None:
        ws = self.wb.add_worksheet(name=global_values.localize.gettext("information"))
        ws.hide_gridlines(2)
        ws.set_column("A:A", 2)
        ws.set_column("B:B", 12)
        ws.set_column("C:C", 12)
        ws.set_column("D:D", 100)
        # Title
        ws.merge_range("B2:D7", global_values.localize.gettext("information_header_title"), self._get_format("information_header"))

        # Title
        ws.merge_range("B9:D9", global_values.localize.gettext("confidentiality"), self._get_format("sub_header"))
        # Key
        ws.merge_range("B10:C10", global_values.localize.gettext("confidentiality_level"), self._get_format("bold"))
        # Value
        ws.write("D10", "FIXME", self._get_format("regular"))

        # Title
        ws.merge_range("B12:D12", global_values.localize.gettext("general_information"), self._get_format("sub_header"))
        # Key
        ws.merge_range("B13:C13", global_values.localize.gettext("date_of_completion"), self._get_format("bold"))
        # Value
        ws.write("D13", today(), self._get_format("regular"))
        # Key
        ws.merge_range("B14:C14", global_values.localize.gettext("used_checklist"), self._get_format("bold"))
        # Value
        ws.write("D14", checklist, self._get_format("regular"))
        # Key
        ws.merge_range("B15:C15", global_values.localize.gettext("tool_version"), self._get_format("bold"))
        # Value
        ws.write("D15", __version__, self._get_format("regular"))
        # Key
        ws.merge_range("B16:C16", global_values.localize.gettext("online_tool_version"), self._get_format("bold"))
        # Value
        ws.write("D16", __url__, self._get_format("regular"))

        # Title
        ws.merge_range("B18:D18", global_values.localize.gettext("audited_equipment"), self._get_format("sub_header"))
        # Key
        ws.merge_range("B19:C19", global_values.localize.gettext("hostname"), self._get_format("bold"))
        # Value
        ws.write("D19", "FIXME", self._get_format("regular"))
        # Key
        ws.merge_range("B20:C20", global_values.localize.gettext("operating_system"), self._get_format("bold"))
        # Value
        ws.write("D20", "FIXME", self._get_format("regular"))
        # Key
        ws.merge_range("B21:C21", global_values.localize.gettext("version"), self._get_format("bold"))
        # Value
        ws.write("D21", "FIXME", self._get_format("regular"))

    def generate_report(self, data: list, checklist: str) -> str:
        self._add_information_worksheet(checklist)
        self._add_synthesis_worksheet(data["categories"][0])
        self._write_results(data["categories"][0])
        self.wb.close()
        self.wb = None
        return self._filename
