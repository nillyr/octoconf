from typing import List

from icecream import ic
import inject

from interactors.report_generator import ReportGeneratorInteractor
from models import CheckResult
from ports import IChecker, IChecklist


class CheckOutputInteractor:
    """
    Receives a list of "CheckResult" and checks the obtained results with the expected results by using the defined verification type.
    """

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
        """
        Launch the verification of the results and send to the report generator use case to ease the manual processing by the user.
        """
        for result in results:
            result.result = self._check_output(
                result.cmd_output.rstrip(), result.expected, result.verification_type
            )
        json_results = self._checklist.get_json_reporting(ic(results))
        return ReportGeneratorInteractor().execute(json_results, is_file=False)
