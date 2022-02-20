# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from icecream import ic
import inject

from octoconf.interactors.report_generator import ReportGeneratorInteractor
from octoconf.ports import IChecker, IChecklist


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
                result.cmd_output, result.expected, result.verification_type
            )
        json_results = self._checklist.get_json_reporting(ic(results))
        json_results = self._checklist.remove_ignore_tag(json_results)
        return ic(json_results)
