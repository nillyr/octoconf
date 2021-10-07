from abc import ABC, abstractmethod


class IChecklist(ABC):
    """
    Interface to work with the checklist provided by the user. Use of an interface so that the code is not dependent on the type of checklist given by the user.
    """
    @abstractmethod
    def parse_checklist(self) -> None:
        pass

    @abstractmethod
    def get_categories(self) -> None:
        pass

    @abstractmethod
    def get_commands(self) -> None:
        pass

    @abstractmethod
    def get_check(self) -> None:
        pass

    @abstractmethod
    def list_collection_cmds(self) -> None:
        pass

    @abstractmethod
    def list_checks(self) -> None:
        pass

    @abstractmethod
    def get_executable(self) -> None:
        pass

    @abstractmethod
    def get_json_reporting(self) -> None:
        pass
