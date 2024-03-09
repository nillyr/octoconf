# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging

import inject

from octoconf.interfaces.report import IReport
from octoconf.utils.logger import *
from octoconf.utils.utils import get_max_len_for_key

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
            headers = ["Themes directory", "Themes", "Source"]
            max_theme_dir_len = get_max_len_for_key(available_templates, "theme_dir")
            max_theme_dir_len = max(len(headers[0]), max_theme_dir_len) + 5

            max_theme_len = get_max_len_for_key(available_templates, "theme")
            max_theme_len = max(len(headers[1]), max_theme_len) + 5

            print(f"{headers[0]: <{max_theme_dir_len}}{headers[1]: <{max_theme_len}}{headers[2]}")
            print("-" * (max_theme_dir_len - 1) + " " + "-" * (max_theme_len - 1) + " " + "-" * (len(headers[2]) + 5))
            for template in available_templates:
                print(f"{template['theme_dir']: <{max_theme_dir_len}}{template['theme']: <{max_theme_len}}{template['source']}")
        except:
            print("No entry found")
            pass

        return 0
