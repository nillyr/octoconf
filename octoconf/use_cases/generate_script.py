# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
from pathlib import Path

import inject

from octoconf.interfaces.baseline import IBaseline
from octoconf.interfaces.generate_script.language_abstract_factory import (
    ILanguageFactory,
)
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


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
        logger.info(f"Running script generation use case")
        baseline_file_path, output_file, platform, utils = args.values()
        logger.debug(
            f"Running with the following arguments: baseline = {baseline_file_path}, output = {output_file}, platform = {platform}, utils = {utils}"
        )
        utils_content = ""

        baseline = self._adapter.load_baseline_from_file(Path(baseline_file_path))
        if baseline is None:
            return 1

        if utils is not None:
            if Path(utils).is_file():
                try:
                    with open(utils, "r") as utils_file:
                        utils_content = "# Import of util file" + self._newline(
                            platform
                        )
                        utils_content += utils_file.read()
                        utils_content += "# Enf of import" + self._newline(platform)
                except:
                    logger.exception("Unable to read util file")
                    return 1

        commands = self._adapter.get_commands(baseline)
        script = self._factory.get_language(platform)

        try:
            with open(output_file, "w", newline=self._newline(platform)) as file:
                content = script.write_script(
                    utils_content, commands, script.write_checks_cmds
                )
                [file.write(x) for x in content]
            return 0
        except:
            logger.exception("Unable to save script")
            return 1
