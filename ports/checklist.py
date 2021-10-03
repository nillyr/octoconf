from abc import ABC, abstractmethod


class IChecklist(ABC):
    @abstractmethod
    def parse_checklist(self) -> None:
        """Used by almost all use cases"""
        pass

    @abstractmethod
    def get_categories(self) -> None:
        """Used by check_archive use case"""
        pass

    @abstractmethod
    def get_commands(self) -> None:
        """Used by collection_script_retrieval use case"""
        pass

    @abstractmethod
    def get_check(self) -> None:
        """Used by check_archive use case"""
        pass

    @abstractmethod
    def list_collection_cmds(self) -> None:
        """Used by checks_runner use case"""
        pass

    @abstractmethod
    def list_checks(self) -> None:
        """Used by checks_runner use case"""
        pass

    @abstractmethod
    def get_executable(self) -> None:
        """Used by checks_runner use case"""
        pass
