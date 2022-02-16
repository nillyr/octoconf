# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from abc import ABC, abstractmethod
from typing import List

from octoconf.models import *


class IChecklist(ABC):
    """
    Interface to work with the checklist provided by the user. Use of an interface so that the code is not dependent on the type of checklist given by the user.
    """

    @abstractmethod
    def parse_checklist(self, checklist_filename) -> None:
        """
        This method must allow to take as input a certain format and convert it to JSON.
        """
        pass

    @abstractmethod
    def get_categories(self) -> List[Category]:
        """
        This method returns a list of categories. See the corresponding model.
        """
        pass

    @abstractmethod
    def get_commands(self) -> List:
        """
        This method returns a list of commands in the following format:
        [
            "category_id": category.id,
            "category_name": category.name,
            "collection_cmds": lst,
            "checks_cmds": checks,
        ]
        """
        pass

    @abstractmethod
    def get_check(self, categories, cmd_id) -> Check:
        """
        This method returns a check whose identifier can be passed as an argument (e.g.: <category_id.checkpoint_id.check_id>).
        """
        pass

    @abstractmethod
    def list_collection_cmds(self) -> List:
        """
        This method returns a list of collection commands for each checkpoint and section.

        The following format should be used:
        [
            {
                "category_name": category["name"],
                "collection_cmd_type": checkpoint["collection_cmd_type"],
                "collection_cmd": checkpoint["collection_cmd"],
            }
        ]
        """
        pass

    @abstractmethod
    def list_checks(self) -> List[Check]:
        """
        This method returns a list of checks. The check identifier must be the concatenation of the category, checkpoint and check identifiers (e.g.: <category_id.checkpoint_id.check_id>).
        """
        pass

    @abstractmethod
    def get_executable(self, cmd_type) -> str:
        """
        This method returns the executable (e.g. /bin/bash) corresponding to the indicated cmd_type (e.g. CMD_EXEC).
        """
        pass

    @abstractmethod
    def get_json_reporting(self, results) -> str:
        """
        This method returns the results of the audit in JSON format.
        """
        pass

    @abstractmethod
    def remove_ignore_tag(self, json_data) -> str:
        """
        This method removes the xml tag that excludes a section of text from the translation.
        """
        pass
