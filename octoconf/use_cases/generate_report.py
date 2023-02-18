# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import json
from pathlib import Path
import sys

from icecream import ic
import inject
from json2xml import json2xml

from octoconf.interfaces import IBaseline, IReportGenerator


class GenerateReportUseCase:
    """
    This use case will allow to call the report generator facilitating the manual processing of the audit results.
    """

    @inject.autoparams("baseline_adapter", "report_generator")
    def __init__(self, baseline_adapter: IBaseline, report_generator: IReportGenerator) -> None:
        self._baseline_adapter = baseline_adapter
        self._report_generator = report_generator

    def _write_json_file(self, filename, data) -> None:
        try:
            filename = filename + "{}".format(".json")
            print(f"[*] Exporting results in JSON format (path: {filename})")
            with open(filename, "w") as json_file:
                json.dump(data, json_file)
            json_file.close()
            print("[+] Done")
        except:
            print("[x] Error", file=sys.stderr)

    def _write_xml_file(self, filename, data) -> None:
        try:
            filename = filename + "{}".format(".xml")
            print(f"[*] Exporting results in XML format (path: {filename})")
            xml = json2xml.Json2xml(
                data,
                wrapper="octoconf-results",
                item_wrap=False,
                attr_type=False,
                pretty=True,
            ).to_xml()
            with open(filename, "w") as xml_file:
                xml_file.write(xml)
            xml_file.close()
            print("[+] Done")
        except:
            print("[x] Error", file=sys.stderr)

    def execute(
            self,
            results,
            baseline_file_path: str,
            is_file: bool = False) -> int:
        if is_file:
            with open(results, "r") as json_file:
                json_results = json.loads(json_file.read())
            json_file.close()
        else:
            baseline = self._baseline_adapter.load_baseline_from_file(Path(baseline_file_path))
            if baseline is None:
                return

            json_results = self._baseline_adapter.map_results_in_baseline(results, baseline)
            json_results = self._baseline_adapter.remove_ignore_translate_tags(json_results)

        filename = self._report_generator.generate_report(
                                                json_results,
                                                baseline_file_path)
        self._write_json_file(filename, json_results)
        self._write_xml_file(filename, json_results)
        return 0
