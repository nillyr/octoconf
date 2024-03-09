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


class ListBaselinesUseCase:
    """
    Prints the list of available baselines.
    """

    @inject.autoparams("adapter")
    def __init__(self, adapter: IBaseline) -> None:
        self._adapter = adapter

    def execute(self) -> int:
        available_baselines = self._adapter.list_available_baselines()
        try:
            headers = ["Title", "Filename", "Source"]
            max_title_len = get_max_len_for_key(available_baselines, "title")
            max_title_len = max(len(headers[0]), max_title_len) + 5

            max_filename_len = get_max_len_for_key(available_baselines, "filename")
            max_filename_len = max(len(headers[1]), max_filename_len) + 5

            print(f"{headers[0]: <{max_title_len}}{headers[1]: <{max_filename_len}}{headers[2]}")
            print("-" * (max_title_len - 1) + " " + "-" * (max_filename_len - 1) + " " + "-" * (len(headers[2]) + 5))
            for baseline in available_baselines:
                print(f"{baseline['title']: <{max_title_len}}{baseline['filename']: <{max_filename_len}}{baseline['source']}")
        except Exception as e:
            logger.exception(e)
            print("No entry found")
            pass

        return 0
