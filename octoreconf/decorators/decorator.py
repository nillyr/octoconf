from abc import ABC, abstractmethod


class Decorator(ABC):
    @abstractmethod
    def decorator(func):
        pass
