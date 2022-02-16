# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import os
import re


class ChecklistsLoader:
    """
    This class allows to load all the checklists of the "checklists" submodule so that they can be used by the users.
    """

    _instance = None
    _checklists: dict = dict()

    def __new__(cls):
        """
        Use of a singleton
        """
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

        regex_yaml_file = r"^.+(?<=\.yaml)$"
        for root, _, files in os.walk(checklists_dir, topdown=False):
            for file in files:
                if re.search(regex_yaml_file, file, re.IGNORECASE | re.MULTILINE):
                    checklist_category = os.path.basename(root)
                    checklist_name = file.split(".")[0]
                    checklist_path = os.path.join(root, file)
                    if checklist_category in self._checklists.keys():
                        self._checklists[checklist_category].update(
                            {checklist_name: checklist_path}
                        )
                    else:
                        self._checklists[checklist_category] = {}
                        self._checklists[checklist_category][
                            checklist_name
                        ] = checklist_path

    def _filter_dict(self, d, f) -> dict:
        """
        Returns the checklists corresponding to the filtered category.
        """
        filtered_dict: dict = dict()
        for key, value in d.items():
            if f(key, value):
                filtered_dict[key] = value
        return filtered_dict

    def get_checklists(self, filter=None) -> dict:
        """
        Returns the nested dictionary containing all the identified checklists.
        """
        if not filter:
            return self._checklists
        else:
            return self._filter_dict(self._checklists, lambda k, v: k == filter)

    def get_checklist_path(self, checklist) -> str:
        """
        Returns the path to the checklist requested by the user.
        """
        checklist_category, checklist_name = checklist.split("/")
        return self._checklists[checklist_category][checklist_name]
