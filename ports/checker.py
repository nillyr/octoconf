from abc import ABC, abstractmethod


class IChecker(ABC):
    @abstractmethod
    def check_exact(self) -> None:
        pass

    @abstractmethod
    def check_regex(self) -> None:
        pass
