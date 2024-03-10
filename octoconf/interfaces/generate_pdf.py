# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional 

from octoconf.entities.baseline import Baseline


class IPDFGenerator(ABC):
    @abstractmethod
    def build_pdf(self, filename: str, output_directory: Path, build_dir: Path, header_file: Optional[str], theme_dir: str, pdf_theme: str) -> None:
        """
        This method must allow the user to re-generate his report
        The user must be able to choose the template / theme to use
        """
        pass

    @abstractmethod
    def generate_pdf(self, filename: str, baseline: Baseline, output_directory: Path, ini_file: Optional[Path], theme_dir: str, pdf_theme: str) -> None:
        """
        This method is called when performing the analyze of the audit evidence
        This method must be able to parse the .ini file in order to initialize the report information
        The output must be the pdf report
        The user must be able to choose the template / theme to use
        """
        pass
