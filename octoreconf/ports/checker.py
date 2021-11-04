from abc import ABC, abstractmethod


class IChecker(ABC):
    """
    Defines the different types of command output verification. Either the command allows to have an output that enables to attest that a = b, or the command does not enable it and in which case a regular expression is used.
    """
    @abstractmethod
    def check_exact(self) -> None:
        pass

    @abstractmethod
    def check_regex(self) -> None:
        pass
