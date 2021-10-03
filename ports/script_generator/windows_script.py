from abc import ABCMeta, abstractmethod
from pathlib import PureWindowsPath
import re


class IWindowsScript(metaclass=ABCMeta):
    _newline = "\r\n"
    _batch_pattern = " > "
    _powershell_pattern = " | Out-File -Path "

    @abstractmethod
    def write_checks_cmds(self, checksdir, content, cmds):
        pass

    @abstractmethod
    def write_script(self, content, platform, callback):
        pass

    @staticmethod
    def preprocess_collection_cmd(basedir, cmd, pattern) -> str:
        output_file = re.split(pattern, cmd)[-1].strip()
        path = basedir / PureWindowsPath(output_file).parent
        replace_path = path / PureWindowsPath(output_file).name
        return re.split(pattern, cmd)[0] + pattern + str(replace_path)
