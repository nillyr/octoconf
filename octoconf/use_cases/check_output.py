# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from icecream import ic
import inject

from octoconf.interfaces import IChecker, IBaseline


class CheckOutputUseCase:
    """
    Receives a list of "CheckResult" and checks the obtained results with the expected results by using the defined verification type.
    """

    @inject.autoparams("checker", "adapter")
    def __init__(self, checker: IChecker, adapter: IBaseline) -> None:
        self._checker = checker
        self._adapter = adapter

    def _check_output(self, cmd_output, expected, verification_type) -> bool:
        if verification_type == "CHECK_REGEX":
            return self._checker.check_regex(cmd_output, expected)
        else:
            return self._checker.check_exact(cmd_output, expected)

    def execute(self, results):
        """
        Launch the verification of the results and send to the report generator use case to ease the manual processing by the user.
        """
        for result in results:
            result.compliant = self._check_output(
                result.output, result.expected, result.verification_type
            )
        return ic(results)
