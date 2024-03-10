# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from octoconf.entities.baseline import Baseline
from octoconf.entities.rule import Rule

class IBaseline(ABC):
    @abstractmethod
    def load_baseline_from_file(self, baseline_file_path) -> Optional[Baseline]:
        """
        This method must allow to take as input a certain format and convert it to JSON.
        """
        pass

    @abstractmethod
    def list_available_baselines(self) -> List:
        """
        This method returns a list of available baselines
        """
        pass

    @abstractmethod
    def export_custom_baselines(self) -> Optional[str]:
        """
        This method allows to export the custom baselines to an archive.
        """
        pass

    @abstractmethod 
    def import_custom_baselines_from_archive(self, archive: str, action: str) -> Optional[Path]:
        """
        This method allows to import the custom baselines from an archive.
        """
        pass

    @abstractmethod
    def map_results_in_baseline(self, rules: List[Rule], baseline: Baseline) -> Baseline:
        """
        This method updates the baseline with the results that are in each rule object
        """
        pass

    @abstractmethod
    def get_commands(self, baseline: Baseline) -> List:
        """
        This method returns a list of commands
        """
        pass

    @abstractmethod
    def get_check(self, baseline: Baseline, rule_filename: str) -> Optional[Rule]:
        """
        This method returns a rule whose identifier can be passed as an argument.
        """
        pass

    @abstractmethod
    def update_rule_with_output_result(self, rule: Rule, output_result: str) -> Rule:
        """
        This method updates the rule with the output result 
        """
        pass


    @abstractmethod
    def remove_ignore_translate_tags(self, baseline: Baseline) -> Baseline:
        """
        This method removes the xml tag that excludes a section of text from the translation.
        """
        pass

    @abstractmethod
    def save_translated_baseline(self, baseline_file_path: Path, baseline: Baseline, output_directory: Path) -> int:
        """
        This method saves the translated baseline to the output directory.
        """
        pass

