# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging

import inject

from octoconf.interfaces.baseline import IBaseline
from octoconf.utils.logger import *

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
            # Arbitrary values (50 & 5)
            max_len = 50
            max_len = [max(max_len, len(d["title"]) + 5) for d in available_baselines][
                0
            ]

            headers = ["Title", "Source"]
            print(f"{headers[0]: <{max_len}}{headers[1]}")
            print("-" * (max_len - 1) + " " + "-" * len(headers[1]))
            for baseline in available_baselines:
                print(f"{baseline['title']: <{max_len}}{baseline['source']}")
        except:
            print("No baseline found")
            pass

        return 0
