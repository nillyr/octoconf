from abc import ABC, abstractmethod


class IReportGenerator(ABC):
    @abstractmethod
    def generate_report(self) -> None:
        pass
