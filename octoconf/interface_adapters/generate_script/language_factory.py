# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging

from octoconf.interface_adapters.generate_script.unix_bash_script import (
    UnixBashScript,
)
from octoconf.interface_adapters.generate_script.windows_powershell_script import (
    WindowsPowershellScript,
)
from octoconf.interfaces.generate_script.language_abstract_factory import (
    ILanguageFactory,
)
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class LanguageFactory(ILanguageFactory):
    @staticmethod
    def get_language(platform: str):
        try:
            if platform.lower() in ("linux", "mac"):
                return UnixBashScript()
            if platform.lower() == "windows":
                return WindowsPowershellScript()
            raise NotImplementedError(
                f"Error: no language implemented for platform {platform}"
            )
        except NotImplementedError as _err:
            logger.exception(f"Error in language selection: {_err}")
        return None
