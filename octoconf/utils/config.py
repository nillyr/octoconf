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
    _absolute_configuration_filepath: str

    def __init__(self) -> None:
        self._cfg_parser = configparser.ConfigParser()
        self._filename = "octoconf.ini"
        self._load_configuration()

    def _init_configuration_file(self, filename: str) -> None:
        with open(filename, "w") as cfg_file:
            content = """[DEFAULT]
# MISC
language = EN

# report colors
header_font_color = FFFFFF
default_font_color = 000000
default_background_color = FFFFFF
header_background_color = 333E4E
sub_header_background_color = 8496AF

# Classification
classification_options = Public, Interne, Confidentiel, Diffusion Restreinte, NC - Non Classifié, C1 - Usage interne, C2 - Diffusion Restreinte, C3 - Secret, Secret, Très Secret, EU Restricted, EU Confidential, EU Secret, EU Top Secret, Restricted, Confidential, Secret, Top Secret
classification_font_color = C51718
classification_background_color = FFFFFF

# level
lvl_minimal = C51718
lvl_intermediary = F1992D
lvl_enhanced = FFCC00
lvl_high = 009644

# status
success = 009644
failed = C51718
to_be_defined = F1992D

[MISC]
#language =

[report_colors]
# Hexadecimal values only
#header_font_color =
#default_font_color =
#default_background_color =
#header_background_color =
#sub_header_background_color =

[classification]
#classification_options =
#classification_font_color =
#classification_background_color =

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
        self._absolute_configuration_filepath = str(cfg_file)
        if not cfg_file.is_file():
            basedir.mkdir(parents=True, exist_ok=True)
            self._init_configuration_file(self._absolute_configuration_filepath)

        self._cfg_parser.read(self._absolute_configuration_filepath)

    def get_config(self, section: str, option: str) -> str:
        try:
            return self._cfg_parser.get(section, option)
        except:
            print(
                f"Error! No option '{option}' in section '{section}'", file=sys.stderr
            )
            return ""

    def get_running_configuration(self) -> str:
        running_configuration: str = ""
        running_configuration = "Configuration file: '%s'\n\n" % (self._absolute_configuration_filepath)
        with open(self._absolute_configuration_filepath, 'r') as configfile:
            running_configuration += "".join(configfile.readlines())
        return running_configuration


    def set_configuration_parameter(self, args) -> None:
        # Update
        self._cfg_parser[args.section][args.parameter] = args.value
        # Commit
        with open(self._absolute_configuration_filepath, 'w') as configfile:
            self._cfg_parser.write(configfile)


sys.modules[__name__] = Config()
