from abc import ABCMeta, abstractmethod
from pathlib import Path
import re


class IUnixScript(metaclass=ABCMeta):
    _newline = "\n"
    _pattern = " > "

    @abstractmethod
    def write_checks_cmds(self, checksdir, content, cmds):
        pass

    @abstractmethod
    def write_script(self, content, platform, callback):
        pass

    @staticmethod
    def preprocess_collection_cmd(basedir, cmd) -> str:
        output_file = re.split(IUnixScript._pattern, cmd)[-1].strip()
        path = basedir / Path(output_file).parent
        replace_path = path / Path(output_file).name
        return (
            re.split(IUnixScript._pattern, cmd)[0]
            + IUnixScript._pattern
            + str(replace_path)
        )
