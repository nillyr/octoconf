# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from abc import ABCMeta, abstractmethod
from pathlib import PurePosixPath
import re

from icecream import ic

from octoconf.adapters.redirector_regex.redirector_regex import RedirectorRegex


class IUnixScript(metaclass=ABCMeta):
    """
    Allows you to generate the collection script for the specified system.
    """

    _newline = "\n"
    _pattern = " >> "
    _regex_pattern = RedirectorRegex.get_redirector_regex("Unix")

    @abstractmethod
    def write_checks_cmds(self, checksdir, content, cmds):
        pass

    @abstractmethod
    def write_script(self, content, platform, callback):
        pass

    @staticmethod
    def preprocess_collection_cmd(basedir, cmd) -> str:
        """
        This method puts the audit proofs in the folder corresponding to the current category. Since the user is not aware of the folder automatically created during the tests, it is not possible to specify the exact path for the output of the files in the checklist.
        """
        cmd_elt = list(filter(None, re.split(IUnixScript._regex_pattern, cmd)))
        for index in range(1, len(cmd_elt), 2):
            path = basedir / PurePosixPath(cmd_elt[index]).parent
            cmd_elt[index] = IUnixScript._pattern + str(
                path / PurePosixPath(cmd_elt[index]).name
            )
            ic(cmd_elt[index])

        return ic("".join(cmd_elt))
