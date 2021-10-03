from icecream import ic
from models import CheckResult
from ports import IChecker
from typing import List
import inject


class CheckOutputInteractor:
    @inject.autoparams("checker")
    def __init__(self, checker: IChecker) -> None:
        self._checker = checker

    def _check_output(self, cmd_output, expected, verification_type) -> bool:
        if verification_type == "CHECK_REGEX":
            return self._checker.check_regex(expected, cmd_output)
        else:
            return self._checker.check_exact(expected, cmd_output)

    def execute(self, results) -> List[CheckResult]:
        for result in results:
            result.result = self._check_output(
                result.cmd_output.rstrip(), result.expected, result.verification_type
            )
        return ic(results)
