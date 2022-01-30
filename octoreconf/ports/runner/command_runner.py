# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from subprocess import Popen, STDOUT, DEVNULL, TimeoutExpired
import sys

from icecream import ic


class ICommandRunner:
    """
    Final code to execute the commands on the system.
    """

    _shell: bool

    def __init__(self, shell) -> None:
        self._shell = shell

    def run(self, cmd, popen_stdout=DEVNULL) -> str:
        """
        This method allows commands to be executed.
        """
        proc = Popen(cmd, stdout=popen_stdout, stderr=STDOUT, shell=self._shell)
        try:
            # timeout: 3 min
            return ic(proc.communicate(timeout=180)[0])
        except TimeoutExpired:
            proc.kill()
            return ""
        except Exception as _err:
            print(f"Error: {_err}.", file=sys.stderr)
