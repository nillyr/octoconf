# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from abc import ABCMeta, abstractmethod


class IOutputRedirectorRegexBuilder(metaclass=ABCMeta):
    @property
    @abstractmethod
    def product(self):
        pass

    @abstractmethod
    def produce_redirectors(self) -> None:
        pass
