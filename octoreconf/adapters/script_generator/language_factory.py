# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import sys

from octoreconf.adapters.script_generator.linux_bash_script import LinuxBashScript
from octoreconf.adapters.script_generator.macos_bash_script import MacOSBashScript
from octoreconf.adapters.script_generator.windows_batch_script import WindowsBatchScript
from octoreconf.adapters.script_generator.windows_powershell_script import (
    WindowsPowershellScript,
)
from octoreconf.ports.script_generator.language_abstract_factory import ILanguageFactory


class LanguageFactory(ILanguageFactory):
    """
    Allows to return the correct factory according to the language desired by the user.
    """

    @staticmethod
    def get_language(platform, language_name):
        try:
            if language_name == "bash":
                return UnixScriptFactory.write_script_for(platform, language_name)
            if language_name in ("batch", "powershell"):
                return WindowsScriptFactory.write_script_for(platform, language_name)
            raise NotImplementedError("Error: not implemented platform or language")
        except NotImplementedError as _err:
            print(_err, file=sys.stderr)
        return None


class UnixScriptFactory:
    @staticmethod
    def write_script_for(platform, language_name):
        # Unused arg: language_name
        try:
            if platform == "linux":
                return LinuxBashScript()
            if platform == "mac":
                return MacOSBashScript()
            raise NotImplementedError("Error: not implemented language")
        except NotImplementedError as _err:
            print(_err, file=sys.stderr)
        return None


class WindowsScriptFactory:
    @staticmethod
    def write_script_for(platform, language_name):
        # Unused arg: platform
        try:
            if language_name == "batch":
                return WindowsBatchScript()
            if language_name == "powershell":
                return WindowsPowershellScript()
            raise NotImplementedError("Error: not implemented language")
        except NotImplementedError as _err:
            print(_err, file=sys.stderr)
        return None
