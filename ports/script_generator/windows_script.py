from abc import ABCMeta, abstractmethod
from pathlib import PureWindowsPath
import re


class IWindowsScript(metaclass=ABCMeta):
    """
    Allows you to generate the collection script for the specified system.
    """

    _newline = "\r\n"
    _batch_pattern = " >> "
    _powershell_pattern = " | Out-File -Append -FilePath "
    _regex_pattern = "\|\s*Out-File\s+(-(Append|FilePath)\s+)*|\s*>+\s*|\s*/(H|cfg)\s*"

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
        output_file = re.split(IWindowsScript._regex_pattern, cmd)[-1].strip()
        path = basedir / PureWindowsPath(output_file).parent
        replace_path = path / PureWindowsPath(output_file).name
        return (
            re.split(IWindowsScript._regex_pattern, cmd)[0]
            + re.search(IWindowsScript._regex_pattern, cmd).group(0)
            + str(replace_path)
        )
