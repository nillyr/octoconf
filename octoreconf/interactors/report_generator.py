# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json

from icecream import ic
import inject

from octoreconf.components.report_generators.report_generator import IReportGenerator


class ReportGeneratorInteractor:
    """
    This use case will allow to call the xlsx report generation component facilitating the manual processing of the audit results.
    """

    @inject.autoparams("xlsx_generator")
    def __init__(self, xlsx_generator: IReportGenerator) -> None:
        self._xlsx_generator = xlsx_generator

    def execute(self, user_input, is_file: bool = False):
        if is_file:
            with open(user_input, "r") as json_file:
                json_results = json.loads(json_file.read())
        else:
            json_results = json.loads(user_input)

        return self._xlsx_generator.generate_report(ic(json_results))
