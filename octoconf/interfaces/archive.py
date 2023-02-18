# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from abc import ABC, abstractmethod


class IArchive(ABC):
    """
    Allows you to work with different types of archives (zip, tar.gz, etc.).
    """

    @abstractmethod
    def checks_files_only(self):
        """
        This method returns only checks files and not collection files.
        """
        pass

    @abstractmethod
    def extract(self):
        """
        This method enables the extraction of an archive.
        """
        pass
