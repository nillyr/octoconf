# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b
from pathlib import Path

from icecream import ic
import inject

from octoconf.interfaces.baseline import IBaseline
from octoconf.interfaces.generate_script.language_abstract_factory import (
    ILanguageFactory,
)


class GenerateScriptUseCase:
    """
    Use case for creating, from a baseline, a script to collect the configuration of the system (or the application) to be audited.
    """

    _newline = lambda _, x: "\n" if x in ("linux", "mac") else "\r\n"

    @inject.autoparams("adapter", "factory")
    def __init__(self, adapter: IBaseline, factory: ILanguageFactory) -> None:
        self._adapter = adapter
        self._factory = factory

    def execute(self, args) -> int:
        baseline_file_path, output_file, platform, utils = ic(args.values())
        utils_content = ""

        baseline = self._adapter.load_baseline_from_file(Path(baseline_file_path))
        if baseline is None:
            return 1

        if utils is not None:
            if Path(utils).is_file():
                try:
                    with open(utils, "r") as utils_file:
                        utils_content = "# Import of util file" + self._newline(platform)
                        utils_content += utils_file.read()
                        utils_content += "# Enf of import" + self._newline(platform)
                    utils_file.close()
                except:
                    return 1

        commands = self._adapter.get_commands(baseline)
        script = self._factory.get_language(platform)

        try:
            with open(output_file, "w", newline=self._newline(platform)) as file:
                content = script.write_script(
                    utils_content, commands, script.write_checks_cmds
                )
                [file.write(x) for x in content]
            file.close()
            return 0
        except:
            return 1
