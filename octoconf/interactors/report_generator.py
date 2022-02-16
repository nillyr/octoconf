# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import json
from xml.dom.minidom import parseString

import dicttoxml
import inject

from octoconf.ports import IReportGenerator
from octoconf.utils import timestamp


class ReportGeneratorInteractor:
    """
    This use case will allow to call the report generator facilitating the manual processing of the audit results.
    """

    @inject.autoparams("report_generator")
    def __init__(self, report_generator: IReportGenerator) -> None:
        self._report_generator = report_generator

    def _write_json_file(self, filename, data) -> None:
        filename += ".json"
        print(f"[*] Exporting results in JSON format (path: {filename})")
        with open(filename, "w") as json_file:
            json.dump(data, json_file)
        print("[+] Done")

    def _write_xml_file(self, filename, data) -> None:
        filename += ".xml"
        print(f"[*] Exporting results in XML format (path: {filename})")
        xml = dicttoxml.dicttoxml(
            data,
            attr_type=True,
            custom_root="octoconf-results",
            item_func=lambda x: x,
        )
        dom = parseString(xml)
        xml_data = dom.toprettyxml()
        with open(filename, "w") as xml_file:
            xml_file.write(xml_data)
        print("[+] Done")

    def execute(self, user_input, is_file: bool = False):
        if is_file:
            with open(user_input, "r") as json_file:
                json_results = json.loads(json_file.read())
        else:
            json_results = json.loads(user_input)

        filename = timestamp() + "_results"
        self._write_json_file(filename, json_results)
        self._write_xml_file(filename, json_results)
        return self._report_generator.generate_report(json_results, filename)
