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


class ExportTemplatesUseCase:
    """
    Exports the templates of the user.
    """

    @inject.autoparams("adapter")
    def __init__(self, adapter: IReport) -> None:
        self._adapter = adapter

    def execute(self) -> int:
        archive_path = self._adapter.export_custom_templates()
        if archive_path:
            print(f"[+] Custom templates saved in: '{archive_path}'")
            return 0
        else:
            return 1

