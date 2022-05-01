# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

from octoconf.adapters.script_generator.linux_bash_script import LinuxBashScript
from octoconf.adapters.script_generator.macos_bash_script import MacOSBashScript
from octoconf.adapters.script_generator.windows_powershell_script import (
    WindowsPowershellScript,
)
from octoconf.ports.script_generator.language_abstract_factory import ILanguageFactory


class LanguageFactory(ILanguageFactory):
    """
    Allows to return the correct factory according to the language desired by the user.
    """

    @staticmethod
    def get_language(platform):
        try:
            if platform.lower() == "linux":
                return LinuxBashScript()
            if platform.lower() == "mac":
               return MacOSBashScript()
            if platform.lower() == "windows":
                return WindowsPowershellScript()
            raise NotImplementedError(f"Error: no language implemented for platform {platform}")
        except NotImplementedError as _err:
            print(_err, file=sys.stderr)
        return None
