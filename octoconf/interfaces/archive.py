# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

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
