# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import re

from octoconf.interfaces.checker import IChecker


class CheckerInterfaceAdapter(IChecker):
    """
    Implementation of the different verification types.
    """

    def __init__(self) -> None:
        pass

    def check_exact(self, output, expected) -> bool:
        return output.lower().rstrip() == expected.lower()

    def check_regex(self, output, expected) -> bool:
        flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
        return re.search(expected, output, flags) is not None
