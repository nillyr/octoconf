# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import re

from octoreconf.ports.checker import IChecker


class CheckerAdapter(IChecker):
    """
    Implementation of the different verification types.
    """

    def __init__(self) -> None:
        pass

    def check_exact(self, expected, output) -> bool:
        return expected.lower() == output.lower().rstrip()

    def check_regex(self, expected, output) -> bool:
        flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
        return re.search(expected, output, flags) is not None
