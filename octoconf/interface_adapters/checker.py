# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
import re

from octoconf.interfaces.checker import IChecker
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class CheckerInterfaceAdapter(IChecker):
    def __init__(self) -> None:
        pass

    def check_exact(self, output, expected) -> bool:
        logger.debug(f"Checking if {output} = {expected}")
        return output.lower().rstrip() == expected.lower()

    def check_regex(self, output, expected) -> bool:
        logger.debug(f"Checking if {output} match with {expected}")
        flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
        return re.search(expected, output, flags) is not None
