# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys
from pathlib import Path

import configparser


class Config:
    """
    This class enables the collection of the configuration defined by the user. If the configuration file is missing, it is created.
    """

    def __init__(self) -> None:
        self._cfg_parser = configparser.ConfigParser()
        self._filename = "octoconf.ini"
        self._load_configuration()

    def _init_configuration_file(self, filename: str) -> None:
        with open(filename, "w") as cfg_file:
            content = """[DEFAULT]
# report colors
font_color = FFFFFF
category_foreground_color = 333E4E
checkpoint_foreground_color = 8496AF

# level
lvl_minimal = C51718
lvl_intermediary = F1992D
lvl_enhanced = FFCC00
lvl_high = 009644

# status
success = 009644
failed = C51718
to_be_defined = F1992D

[report_colors]
# Hexadecimal values only
#font_color =
#category_foreground_color =
#checkpoint_foreground_color =

[level_colors]
# level
#lvl_minimal =
#lvl_intermediary =
#lvl_enhanced =
#lvl_high =

[status_colors]
# Hexadecimal values only
#success =
#failed =
#to_be_defined =
"""
            cfg_file.write(content)

    def _load_configuration(self) -> None:
        basedir = Path.home() / ".config" / "octoconf"
        cfg_file = Path(basedir / self._filename)
        if not cfg_file.is_file():
            basedir.mkdir(parents=True, exist_ok=True)
            self._init_configuration_file(str(cfg_file))

        self._cfg_parser.read(str(cfg_file))

    def get_config(self, section: str, option: str) -> str:
        try:
            return self._cfg_parser.get(section, option)
        except:
            print(
                f"Error! No option '{option}' in section '{section}'", file=sys.stderr
            )
            return ""


sys.modules[__name__] = Config()
