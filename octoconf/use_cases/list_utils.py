# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging

import inject

from octoconf.interfaces.baseline import IBaseline
from octoconf.utils.logger import *
from octoconf.utils.utils import get_max_len_for_key

logger = logging.getLogger(__name__)


class ListUtilsUseCase:
    """
    Prints the list of available utility scripts.
    """

    @inject.autoparams("adapter")
    def __init__(self, adapter: IBaseline) -> None:
        self._adapter = adapter

    def execute(self) -> int:
        available_util_scripts = self._adapter.list_available_utils_scripts()
        try:
            headers = ["Utility script", "Source"]
            max_filename_len = get_max_len_for_key(available_util_scripts, "filename")
            max_filename_len = max(len(headers[0]), max_filename_len) + 5

            print(f"{headers[0]: <{max_filename_len}}{headers[1]}")
            print("-" * (max_filename_len - 1) + " " + "-" * (len(headers[1]) + 5))
            for util_script in available_util_scripts:
                print(f"{util_script['filename']: <{max_filename_len}}{util_script['source']}")
        except Exception as e:
            logger.exception(e)
            print("No entry found")
            pass

        return 0
