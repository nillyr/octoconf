# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from octoconf.entities.baseline import Baseline
from octoconf.entities.rule import Rule

class IBaseline(ABC):
    """
    Interface to work with the baseline provided by the user. Use of an interface so that the code is not dependent on the type of baseline given by the user.
    """

    @abstractmethod
    def load_baseline_from_file(self, baseline_filename) -> Baseline:
        """
        This method must allow to take as input a certain format and convert it to JSON.
        """
        pass

    @abstractmethod
    def get_commands(self) -> List:
        """
        This method returns a list of commands
        """
        pass

    @abstractmethod
    def get_check(self, baseline: Baseline, rule_filename: str) -> Rule:
        """
        This method returns a rule whose identifier can be passed as an argument.
        """
        pass

    @abstractmethod
    def map_results_in_baseline(self, rule: Rule, baseline: Baseline) -> Baseline:
        """
        This method updates the baseline with the obtaines results that are in the 'rule' object
        """
        pass

    @abstractmethod
    def remove_ignore_translate_tags(self, json_data) -> str:
        """
        This method removes the xml tag that excludes a section of text from the translation.
        """
        pass

    @abstractmethod
    def save_translated_baseline(self, baseline_file_path: Path, baseline: Baseline, output_dir: Path) -> int:
        pass
