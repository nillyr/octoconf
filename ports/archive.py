from abc import ABC, abstractmethod


class IArchive(ABC):
    """
    Allows you to work with different types of archives (zip, tar.gz, etc.).
    """

    @abstractmethod
    def checks_files_only(self):
        pass

    @abstractmethod
    def extract(self):
        pass
