# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator, Optional


class IArchive(ABC):
    @abstractmethod
    def checks_files_only(self, members) -> Generator:
        """
        This method returns only checks files and not collection files.
        """
        pass

    @abstractmethod
    def extract(self, archive) -> Optional[Path]:
        """
        This method enables the extraction of an archive (zip and tar.gz) and returns the path of the extracted files.
        """
        pass
