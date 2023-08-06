# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
from typing import List

import inject

from octoconf.entities.rule import Rule
from octoconf.interfaces.baseline import IBaseline
from octoconf.interfaces.checker import IChecker
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


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

    def execute(self, results: List[Rule]) -> List[Rule]:
        """
        Launch the verification of the results and send to the report generator use case to ease the manual processing by the user.
        """
        logger.info(f"Running check output use case")
        for result in results:
            result.compliant = self._check_output(
                result.output, result.expected, result.verification_type
            )
        return results
