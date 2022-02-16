# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import os
import sys

import configparser


class Config(configparser.ConfigParser):
    """
    This class enables the collection of the configuration defined by the user. If the configuration file is missing, it is created.
    """

    _instance = None
    _already_loaded = False
    _filename = "octoconf.ini"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __call__(self) -> None:
        if not self._already_loaded:
            self._load_configuration()
            self._already_loaded = not self._already_loaded
        return

    def _init_configuration_file(self, path, config_file) -> None:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, config_file), "w") as cfg_file:
            content = """[DEFAULT]
# report colors
font_color = FFFFFF
category_foreground_color = 333E4E
checkpoint_foreground_color = 8496AF

# severity
s_info = 2C68C4
s_low = F5B76C
s_medium = F1992D
s_high = C51718

# status
success = 009644
failed = C51718
to_be_defined = F1992D

[report_colors]
# Hexadecimal values only
#font_color =
#category_foreground_color =
#checkpoint_foreground_color =

[severity_colors]
# Hexadecimal values only
#s_info =
#s_low =
#s_medium =
#s_high =

[status_colors]
# Hexadecimal values only
#success =
#failed =
#to_be_defined =
"""
            cfg_file.write(content)

    def _load_configuration(self) -> None:
        basedir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../.config/")
        )
        config_file = os.path.abspath(os.path.join(basedir, self._filename))
        if not os.path.isfile(config_file):
            self._init_configuration_file(basedir, config_file)

        self.read(config_file)

    def get_config(self, section, option) -> str:
        try:
            return self.get(section, option)
        except:
            print(
                f"Error! No option '{option}' in section '{section}'", file=sys.stderr
            )
            return ""
