from icecream import ic
from components.report_generators.report_generator import IReportGenerator
import inject
import json


class ReportGeneratorInteractor:
    @inject.autoparams("xlsx_generator")
    def __init__(self, xlsx_generator: IReportGenerator) -> None:
        self._xlsx_generator = xlsx_generator

    def execute(self, user_input, is_file: bool = False):
        if is_file:
            with open(user_input, "r") as json_file:
                json_results = json.loads(json_file.read())
        else:
            json_results = json.loads(user_input)

        return self._xlsx_generator.generate_report(json_results)
