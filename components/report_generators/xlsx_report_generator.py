from components.report_generators.report_generator import IReportGenerator
from icecream import ic
from utils import *
import json
import xlsxwriter


const.COLORS = {
    "WHITE": "FFFFFF",
    "DARK_BLUE": "333E4E",
    "LIGHT_BLUE": "8496AF",
    "REGULAR_GREEN": "009644",
    "REGULAR_ORANGE": "F1992D",
    "REGULAR_RED": "C51718",
}


class XlsxGenerator(IReportGenerator):
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

    def _get_uncertain_result_format(self, workbook: xlsxwriter.workbook.Workbook):
        return workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_color": const.COLORS["REGULAR_ORANGE"],
            }
        )

    def _write_results(self, workbook: xlsxwriter.workbook.Workbook, data):
        for item in data:
            for category in item["categories"]:
                worksheet = workbook.add_worksheet(name=category["name"])
                worksheet.set_column("A:D", 20)
                worksheet.set_row(0, 25)
                worksheet.merge_range(
                    "A1:D1", category["name"], self._get_category_format(workbook)
                )
                checkpoint_row = 2
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
                            elif check["result"] == False:
                                worksheet.write(
                                    f"D{check_row}",
                                    "PASSED",
                                    self._get_failed_result_format(workbook),
                                )
                            else:
                                worksheet.write(
                                    f"D{check_row}",
                                    "N/A",
                                    self._get_uncertain_result_format(workbook),
                                )
                            check_row += 1
                            checkpoint_row = check_row
                        else:
                            worksheet.write(
                                f"D{check_row}",
                                "N/A",
                                self._get_uncertain_result_format(workbook),
                            )
                            check_row += 1
                            checkpoint_row = check_row

    def _generate_charts(self, workbook: xlsxwriter.workbook.Workbook):
        # TODO: (https://xlsxwriter.readthedocs.io/working_with_charts.html)
        pass

    def generate_report(self, data):
        filename = timestamp() + "_results"
        workbook = xlsxwriter.Workbook(filename + ".xlsx")
        self._write_results(workbook, data)
        self._generate_charts(workbook)
        workbook.close()

        filename += ".json"
        print(f"[*] Exporting results in JSON format (path: {filename})")
        with open(filename, "w") as json_file:
            json.dump(data, json_file)
        print("[+] Done")
        return
