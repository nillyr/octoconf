# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoconf
# @since 1.0.0b

from subprocess import PIPE, DEVNULL
import sys

from icecream import ic

from octoconf.ports.runner.command_runner import ICommandRunner


class UnixCommandRunner(ICommandRunner):
    """
    Class allowing to execute commands on Unix/Linux systems.
    """

    def __init__(self) -> None:
        ICommandRunner.__init__(self, shell=True)

    def exec(self, cmd, cmd_type, is_check=False) -> str:
        """
        Exec the command
        """
        # ignore cmd_type
        _ = cmd_type
        # When the collection commands are run, the output is redirected to a file. No need to have it. On the other hand, when the checks are performed, stdout is needed
        popen_stdout = PIPE if is_check else DEVNULL
        try:
            stdout = self.run(cmd, popen_stdout)
            return ic(str(stdout.decode("utf-8")))
        except AttributeError:
            # This case occurs when popen_stdout is set to DEVNULL
            return ""
        except Exception as _err:
            print(f"Error: {_err}.", file=sys.stderr)
