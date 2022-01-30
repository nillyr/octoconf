# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from abc import ABC, abstractmethod
from typing import List

from octoreconf.models import *


class IChecklist(ABC):
    """
    Interface to work with the checklist provided by the user. Use of an interface so that the code is not dependent on the type of checklist given by the user.
    """

    @abstractmethod
    def parse_checklist(self) -> None:
        pass

    @abstractmethod
    def get_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def get_commands(self) -> List:
        pass

    @abstractmethod
    def get_check(self) -> Check:
        pass

    @abstractmethod
    def list_collection_cmds(self) -> List:
        pass

    @abstractmethod
    def list_checks(self) -> List[Check]:
        pass

    @abstractmethod
    def get_executable(self) -> str:
        pass

    @abstractmethod
    def get_json_reporting(self) -> str:
        pass
