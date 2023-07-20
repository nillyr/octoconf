# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

from icecream import ic


class Debug:
    """
    Configuration of the external package icecream.
    """

    def __init__(self) -> None:
        self.debug = False
        ic.disable()

    def set_debug(self, value: bool) -> None:
        """
        This method is called when the -d argument is present.
        """
        self.debug = value
        if self.debug:
            ic.enable()
            ic.configureOutput(prefix="Debug:", includeContext=True)
            return


sys.modules[__name__] = Debug()
