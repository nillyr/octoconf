# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from abc import ABCMeta, abstractmethod
from pathlib import PureWindowsPath
import re

from icecream import ic

from octoconf.interface_adapters.redirector_regex.redirector_regex import (
    RedirectorRegex,
)


class IWindowsScript(metaclass=ABCMeta):
    """
    Allows you to generate the collection script for the specified system.
    """

    _newline = "\n"
    _powershell_pattern = " | Out-File -Encoding utf8 -Append -FilePath "
    _regex_pattern = RedirectorRegex.get_redirector_regex("Windows")

    @abstractmethod
    def write_checks_cmds(self, checksdir, content, cmds):
        pass

    @abstractmethod
    def write_script(self, utils_content, content, platform, callback):
        pass

    @staticmethod
    def preprocess_collection_cmd(basedir, collection_cmd) -> str:
        """
        This method puts the audit proofs in the folder corresponding to the current category. Since the user is not aware of the folder automatically created during the tests, it is not possible to specify the exact path for the output of the files in the baseline.
        """

        matches = re.finditer(IWindowsScript._regex_pattern, collection_cmd)
        redirectors = []
        for _, match in enumerate(matches, start=1):
            redirectors.append(match.group())

        cmd_elt = list(
            filter(None, re.split(IWindowsScript._regex_pattern, collection_cmd))
        )

        for index in range(1, len(cmd_elt)):
            # 0 out_file
            # 1..n other commands if any
            splited_cmd_elt = cmd_elt[index].split(sep=";", maxsplit=1)
            out_file = splited_cmd_elt[0].lstrip()

            out_file = out_file.split(sep=IWindowsScript._newline, maxsplit=1)
            out_file[0] = re.sub(r"(^\\|/)", "", out_file[0], count=1)

            new_outfile_path = str(basedir / PureWindowsPath(out_file[0]))
            if len(out_file) > 1:
                new_outfile_path += IWindowsScript._newline + out_file[-1]

            if len(splited_cmd_elt) > 1:
                new_outfile_path += "; "

            joined_cmd_elt = (
                new_outfile_path
                + IWindowsScript._newline.join(splited_cmd_elt[1:]).lstrip()
            )

            cmd_elt[index] = redirectors[index - 1] + joined_cmd_elt

        return ic("".join(cmd_elt))
