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


class ImportBaselinesUseCase:
    """
    Prints the list of available baselines.
    """

    @inject.autoparams("adapter")
    def __init__(self, adapter: IBaseline) -> None:
        self._adapter = adapter

    def execute(self, archive: str, action: str) -> int:
        logger.info("Importing custom baselines from user provided archive")
        path = self._adapter.import_custom_baselines_from_archive(archive, action)
        if path:
            print(f"[+] Custom baselines imported in {path}")
            return 0

        print("[x] Error! Unable to import your baselines. Data remains unchanged.")
        return 1
