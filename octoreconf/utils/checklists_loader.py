# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import os
import re
from threading import Lock


class ChecklistsLoader:
    """
    This class allows to load all the checklists of the "checklists" submodule so that they can be used by the users.
    """

    _instance = None
    _lock: Lock = Lock()
    _checklists: dict = dict()

    def __new__(cls):
        """
        Use of a singleton
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __call__(self) -> None:
        self._load_checklists()

    def _load_checklists(self) -> None:
        """
        Browse the checklist folder and add the checklists to the dictionary.
        """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        checklists_dir = os.path.join(base_dir, "checklists/checklists")

        regex_hjson_file = r"^.+(?<=\.hjson)$"
        for root, _, files in os.walk(checklists_dir, topdown=False):
            for file in files:
                if re.search(regex_hjson_file, file, re.IGNORECASE | re.MULTILINE):
                    checklist_category = os.path.basename(root)
                    checklist_name = file.split(".")[0]
                    checklist_path = os.path.join(root, file)

                    self._checklists[checklist_category] = {}
                    self._checklists[checklist_category][
                        checklist_name
                    ] = checklist_path

    def get_checklists(self) -> dict:
        """
        Returns the nested dictionary containing all the identified checklists.
        """
        return self._checklists

    def get_checklist_path(self, checklist) -> str:
        """
        Returns the path to the checklist requested by the user.
        """
        checklist_category, checklist_name = checklist.split("/")
        return self._checklists[checklist_category][checklist_name]
