# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import platform
import sys

from octoconf.adapters.runner.unix_command_runner import UnixCommandRunner
from octoconf.adapters.runner.windows_command_runner import WindowsCommandRunner
from octoconf.ports.runner.command_runner_abstract_factory import (
    ICommandRunnerFactory,
)


class CommandRunnerFactory(ICommandRunnerFactory):
    """
    Implementation of the abstract factory.
    """

    @staticmethod
    def get_runner():
        """
        Returns the corresponding class according to the system.
        """
        try:
            if platform.system() == "Windows":
                return WindowsCommandRunner()
            elif platform.system() in ("Linux", "Darwin"):
                return UnixCommandRunner()
            else:
                raise NotImplementedError("Error: not implemented system")
        except NotImplementedError as _err:
            print(_err, file=sys.stderr)
        return None
