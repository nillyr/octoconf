# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from abc import ABC, abstractmethod


class IChecker(ABC):
    """
    Defines the different types of command output verification. Either the command allows to have an output that enables to attest that a = b, or the command does not enable it and in which case a regular expression is used.
    """

    @abstractmethod
    def check_exact(self) -> bool:
        """
        This method returns true if the output value = expected value.
        """
        pass

    @abstractmethod
    def check_regex(self) -> bool:
        """
        This method returns true if there is a match in the output.
        """
        pass
