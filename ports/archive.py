from abc import ABC, abstractmethod


class IArchive(ABC):
    @abstractmethod
    def checks_files_only(self):
        pass

    @abstractmethod
    def extract(self):
        pass
