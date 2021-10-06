from icecream import ic
from interactors.report_generator import ReportGeneratorInteractor
from models import CheckResult
from ports import IChecker, IChecklist
from typing import List
import inject


class CheckOutputInteractor:
    @inject.autoparams("checker", "checklist")
    def __init__(self, checker: IChecker, checklist: IChecklist) -> None:
        self._checker = checker
        self._checklist = checklist

    def _check_output(self, cmd_output, expected, verification_type) -> bool:
        if verification_type == "CHECK_REGEX":
            return self._checker.check_regex(expected, cmd_output)
        else:
            return self._checker.check_exact(expected, cmd_output)

    def execute(self, results):
        for result in results:
            result.result = self._check_output(
                result.cmd_output.rstrip(), result.expected, result.verification_type
            )
        json_results = self._checklist.get_json_reporting(ic(results))
        return ReportGeneratorInteractor().execute(json_results, is_file=False)
