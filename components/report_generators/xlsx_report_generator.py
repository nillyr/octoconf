import json

from icecream import ic
import xlsxwriter

from components.report_generators.report_generator import IReportGenerator
from utils import const, timestamp


const.COLORS = {
    "WHITE": "FFFFFF",
    "DARK_BLUE": "333E4E",
    "LIGHT_BLUE": "8496AF",
    "REGULAR_GREEN": "009644",
    "REGULAR_ORANGE": "F1992D",
    "REGULAR_RED": "C51718",
}


class XlsxGenerator(IReportGenerator):
    def __init__(self):
        self._synthesis = dict()

    def _get_category_format(self, workbook: xlsxwriter.workbook.Workbook):
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": const.COLORS["WHITE"],
                "fg_color": const.COLORS["DARK_BLUE"],
            }
        )

    def _get_checkpoint_format(self, workbook: xlsxwriter.workbook.Workbook):
        return workbook.add_format(
            {
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": const.COLORS["WHITE"],
                "fg_color": const.COLORS["LIGHT_BLUE"],
            }
        )

    def _get_check_format(self, workbook: xlsxwriter.workbook.Workbook):
        return workbook.add_format(
            {
                "border": 1,
                "align": "left",
                "valign": "vcenter",
            }
        )

    def _get_passed_result_format(self, workbook: xlsxwriter.workbook.Workbook):
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": const.COLORS["REGULAR_GREEN"],
            }
        )

    def _get_failed_result_format(self, workbook: xlsxwriter.workbook.Workbook):
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": const.COLORS["REGULAR_RED"],
            }
        )

    def _get_uncertain_result_format(self,
                                        workbook: xlsxwriter.workbook.Workbook):
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": const.COLORS["REGULAR_ORANGE"],
            }
        )

    def _write_results(self,
                        workbook: xlsxwriter.workbook.Workbook,
                        data: list):
        for item in data:
            for category in item["categories"]:
                worksheet = workbook.add_worksheet(name=category["name"])
                worksheet.set_column("A:D", 20)
                worksheet.set_row(0, 25)
                worksheet.merge_range(
                    "A1:D1", category["name"], self._get_category_format(workbook)
                )
                checkpoint_row = 2
                nb_passed, nb_failed, nb_na = 0, 0, 0
                for checkpoint in category["checkpoints"]:
                    worksheet.merge_range(
                        f"A{checkpoint_row}:C{checkpoint_row}",
                        checkpoint["title"],
                        self._get_checkpoint_format(workbook),
                    )
                    worksheet.write(
                        f"D{checkpoint_row}",
                        "Result",
                        self._get_checkpoint_format(workbook),
                    )
                    check_row = checkpoint_row + 1
                    for check in checkpoint["checks"]:
                        worksheet.merge_range(
                            f"A{check_row}:C{check_row}",
                            check["description"],
                            self._get_check_format(workbook),
                        )
                        if "result" in check:
                            if check["result"] == True:
                                worksheet.write(
                                    f"D{check_row}",
                                    "PASSED",
                                    self._get_passed_result_format(workbook),
                                )
                                nb_passed += 1
                            elif check["result"] == False:
                                worksheet.write(
                                    f"D{check_row}",
                                    "FAILED",
                                    self._get_failed_result_format(workbook),
                                )
                                nb_failed += 1
                            else:
                                worksheet.write(
                                    f"D{check_row}",
                                    "N/A",
                                    self._get_uncertain_result_format(workbook),
                                )
                                nb_na += 1
                            check_row += 1
                            checkpoint_row = check_row
                        else:
                            worksheet.write(
                                f"D{check_row}",
                                "N/A",
                                self._get_uncertain_result_format(workbook),
                            )
                            nb_na += 1
                            check_row += 1
                            checkpoint_row = check_row

                self._synthesis[category["name"]] = {
                    "PASSED": nb_passed,
                    "FAILED": nb_failed,
                    "N/A": nb_na,
                }

    def _generate_synthesis(self,
                            workbook: xlsxwriter.workbook.Workbook,
                            worksheet: xlsxwriter.worksheet.Worksheet) -> int:
        worksheet.set_column("A:G", 15)
        worksheet.set_row(0, 25)
        worksheet.merge_range("A1:G1", "Synthesis", self._get_category_format(workbook))
        worksheet.merge_range(
            "A2:C2", "Categories", self._get_checkpoint_format(workbook)
        )
        worksheet.write("D2", "# PASSED", self._get_checkpoint_format(workbook))
        worksheet.write("E2", "# FAILED", self._get_checkpoint_format(workbook))
        worksheet.write("F2", "# N/A", self._get_checkpoint_format(workbook))
        worksheet.write("G2", "% Percentage", self._get_checkpoint_format(workbook))

        row = 2
        for key, value in self._synthesis.items():
            row += 1
            ic(key, value["PASSED"], value["FAILED"], value["N/A"])
            worksheet.merge_range(
                f"A{row}:C{row}",
                key,
                self._get_check_format(workbook),
            )
            worksheet.write(
                f"D{row}",
                value["PASSED"],
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
            worksheet.write(
                f"G{row}",
                (value["PASSED"] * 100)
                / (value["PASSED"] + value["FAILED"] + value["N/A"]),
                self._get_check_format(workbook),
            )
        return row

    def _generate_charts(self,
                            workbook: xlsxwriter.workbook.Workbook,
                            worksheet: xlsxwriter.worksheet.Worksheet,
                            last_row: int):
        # Radar
        radar_chart = workbook.add_chart({"type": "radar", "subtype": "filled"})
        radar_chart.set_title({"name": "Configuration coverage summary"})
        radar_chart.add_series(
            {
                "name": "=Synthesis!$G$2",
                "categories": f"=Synthesis!$A$3:$A${last_row + 1}",
                "values": f"=Synthesis!$G$3:$G${last_row + 1}",
                "fill": {"color": "green"},
            }
        )
        worksheet.insert_chart("J1", radar_chart)

        # Column
        column_chart = workbook.add_chart({"type": "column"})
        column_chart.set_title({"name": "Configuration coverage summary"})
        column_chart.set_x_axis({"name": "Categories"})
        column_chart.set_y_axis({"name": "Number of checks"})
        column_chart.add_series(
            {
                "name": "=Synthesis!$D$2",
                "categories": f"=Synthesis!$A$3:$A${last_row}",
                "values": f"=Synthesis!$D$3:$D${last_row}",
                "fill": {"color": "green"},
            }
        )
        column_chart.add_series(
            {
                "name": "=Synthesis!$E$2",
                "categories": f"=Synthesis!$A$3:$A${last_row}",
                "values": f"=Synthesis!$E$3:$E${last_row}",
                "fill": {"color": "red"},
            }
        )
        column_chart.add_series(
            {
                "name": "=Synthesis!$F$2",
                "categories": f"=Synthesis!$A$3:$A${last_row}",
                "values": f"=Synthesis!$F$3:$F${last_row}",
                "fill": {"color": "blue"},
            }
        )
        column_chart.set_table({"show_keys": True})
        column_chart.set_legend({"position": "none"})
        worksheet.insert_chart(f"A{last_row + 5}", column_chart)

    def generate_report(self, data: list):
        filename = timestamp() + "_results"
        workbook = xlsxwriter.Workbook(filename + ".xlsx")
        worksheet = workbook.add_worksheet(name="Synthesis")
        self._write_results(workbook, data)
        last_row = self._generate_synthesis(workbook, worksheet)
        self._generate_charts(workbook, worksheet, last_row)
        workbook.close()

        filename += ".json"
        print(f"[*] Exporting results in JSON format (path: {filename})")
        with open(filename, "w") as json_file:
            json.dump(data, json_file)
        print("[+] Done")
        return
