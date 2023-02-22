# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

from octoconf.interface_adapters.generate_script.unix_bash_script import (
    UnixBashScript,
)
from octoconf.interface_adapters.generate_script.windows_powershell_script import (
    WindowsPowershellScript,
)
from octoconf.interfaces.generate_script.language_abstract_factory import (
    ILanguageFactory,
)


class LanguageFactory(ILanguageFactory):
    """
    Allows to return the correct factory according to the language desired by the user.
    """

    @staticmethod
    def get_language(platform):
        try:
            if platform.lower() in ("linux", "mac"):
                return UnixBashScript()
            if platform.lower() == "windows":
                return WindowsPowershellScript()
            raise NotImplementedError(
                f"Error: no language implemented for platform {platform}"
            )
        except NotImplementedError as _err:
            print(_err, file=sys.stderr)
        return None
