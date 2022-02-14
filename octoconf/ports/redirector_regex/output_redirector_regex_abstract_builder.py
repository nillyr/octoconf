# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoconf
# @since 1.0.0b

from abc import ABCMeta, abstractmethod


class IOutputRedirectorRegexBuilder(metaclass=ABCMeta):
    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_redirectors(self) -> None:
        pass