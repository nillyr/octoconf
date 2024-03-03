# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging

import inject

from octoconf.interfaces.report import IReport
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class ListTemplatesUseCase:
    """
    Prints the list of available templates.
    """

    @inject.autoparams("adapter")
    def __init__(self, adapter: IReport) -> None:
        self._adapter = adapter

    def execute(self) -> int:
        available_templates = self._adapter.list_available_templates()
        try:
            # Arbitrary values (24 & 5)
            max_len = 24
            max_len = [max(max_len, len(d["theme_dir"]) + 5) for d in available_templates][
                0
            ]
            max_theme_len = 24
            max_theme_len = [max(max_theme_len, len(d["theme"]) + 5) for d in available_templates][0]

            headers = ["Themes directory", "Themes", "Source"]
            print(f"{headers[0]: <{max_len}}{headers[1]: <{max_theme_len}}{headers[2]}")
            print("-" * (max_len - 1) + " " + "-" * (max_theme_len - 1) + " " + "-" * (len(headers[2]) + 5) )
            for template in available_templates:
                print(f"{template['theme_dir']: <{max_len}}{template['theme']: <{max_theme_len}}{template['source']}")
        except:
            print("No entry found")
            pass

        return 0
