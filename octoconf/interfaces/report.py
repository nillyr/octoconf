# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from octoconf.entities.baseline import Baseline

class IReport(ABC):
    @abstractmethod 
    def generate_csv(self, filename: str, results: Baseline, output_dir: Any) -> int:
        """
        Generate a CSV report from the results of the baseline.
        """
        pass

    @abstractmethod 
    def regenerate_report(self, input_file: Path, args: Any) -> int:
        """
        Regenerate a report from the results of the baseline.
        """
        pass

    @abstractmethod
    def generate_report(self, results: Baseline, args: Any) -> int:
        """
        Generate a report from the results of the baseline.
        """
        pass

    @abstractmethod 
    def list_available_templates(self) -> list:
        """
        List the available templates.
        """
        pass

    @abstractmethod 
    def export_custom_templates(self) -> Optional[str]:
        """
        Export the custom templates.
        """
        pass

    @abstractmethod 
    def import_custom_templates_from_archive(self, archive: str, action: str) -> Optional[Path]:
        """
        Import the custom templates.
        """
        pass
