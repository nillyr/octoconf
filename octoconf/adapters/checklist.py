# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from enum import Enum
import json
import re
import sys
from typing import List

from icecream import ic
import yaml

from octoconf.components.json_encoders.checklist import ChecklistJsonEncoder
from octoconf.models import *
from octoconf.ports.checklist import IChecklist


class NoValue(Enum):
    """
    Enables to set the enumeration values in string form and thus reduce the number of lines of code.
    """

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)


class ChecklistAdapter(IChecklist):
    """
    Implementation of the interface allowing to work with the type of checklist.
    """

    _instance = None
    _checklist = None

    class CmdType(NoValue):
        """
        Definition of the different cmd_types that can be present in a checklist.
        """

        # WINDOWS
        AUDIT_POWERSHELL = "powershell.exe"
        # UNIX
        CMD_EXEC = "/bin/bash"

    def __new__(cls):
        """
        As some methods can have a high consumption of resources (BigO notation), the singleton design pattern is used to limit the consumption of resources.
        """
        if cls._instance is None:
            cls._instance = super(IChecklist, cls).__new__(cls)
        return cls._instance

    def parse_checklist(self, checklist_filename) -> None:
        """
        Retrieves the data present in the checklist provided as an argument.
        """
        if self._checklist is None:
            categories = []
            checklist = dict(categories=categories)
            with open(checklist_filename, "r") as file:
                for data in yaml.load_all(file, Loader=yaml.BaseLoader):
                    checklist["categories"].append(data)
                    self._checklist = json.loads(json.dumps(checklist))

    def get_executable(self, cmd_type) -> str:
        """
        Returns the value of the cmd_type.
        """
        if cmd_type == "AUDIT_POWERSHELL":
            return self.CmdType.AUDIT_POWERSHELL.value
        if cmd_type == "CMD_EXEC":
            return self.CmdType.CMD_EXEC.value
        return

    def _create_empty_check(self, id) -> Check:
        """
        This method enables to create an object of type "Check" which does not contain any result. The objective is to represent the collection in the result list so that it is not forgotten to add it to the final report.
        """
        return Check(
            id=id,
            title="FIXME",
            description="",
            type="",
            cmd="",
            expected="FIXME",
            verification_type="",
            result=False,
            severity="info",
            recommendation_on_failed="",
        )

    def get_categories(self) -> List[Category]:
        """
        Puts the data of the checklist in the different defined entities.
        """
        categories_list = []
        for category in self._checklist["categories"][0]:
            checkpoints_list = []
            for checkpoint in category["checkpoints"]:
                checks_list = []
                if checkpoint["collect_only"] in ("true", "True"):
                    checks_list.append(self._create_empty_check(1))
                else:
                    for check in checkpoint["checks"]:
                        checks_list.append(Check(**check))
                checkpoint["checks"] = checks_list
                checkpoints_list.append(Checkpoint(**checkpoint))
            category["checkpoints"] = checkpoints_list
            categories_list.append(Category(**category))

        return categories_list

    def get_commands(self) -> List:
        """
        Returns all the commands (collection and checks) of the different categories in the form of a list.
        """
        categories = self.get_categories()
        commands = []
        for category in categories:
            checks, lst = [], []
            checkpoints = category.checkpoints
            for checkpoint in range(len(checkpoints)):
                if checkpoints[checkpoint].collection_cmd is not None:
                    lst.append(checkpoints[checkpoint].collection_cmd)
                for check in range(len(checkpoints[checkpoint].checks)):
                    checks.append(
                        [
                            "%s" % category.id
                            + ".%s" % checkpoints[checkpoint].id
                            + ".%s" % checkpoints[checkpoint].checks[check].id,
                            checkpoints[checkpoint].checks[check].cmd,
                        ]
                    )
            commands.append(
                {
                    "category_id": category.id,
                    "category_name": category.name,
                    "collection_cmds": lst,
                    "checks_cmds": checks,
                }
            )
        return commands

    def get_check(self, categories, cmd_id) -> Check:
        """
        Given an identifier of the form category_id[.]checkpoint_id[.]check_id, returns the corresponding check entity from the checklist.
        """
        category_id, checkpoint_id, check_id = (
            int(cmd_id.split(".")[0]),
            int(cmd_id.split(".")[1]),
            int(cmd_id.split(".")[2]),
        )
        check: Check = None
        try:
            check = (
                categories[category_id - 1]
                .checkpoints[checkpoint_id - 1]
                .checks[check_id - 1]
            )
        except IndexError as _err:
            print(
                f"Error: Check not found. Are you using the correct checklist?{_err}",
                file=sys.stderr,
            )
            pass
        finally:
            return check

    def list_collection_cmds(self) -> List:
        """
        Returns the set of checklist commands for collecting audit proofs.
        """
        collection_cmds = []
        for category in self._checklist["categories"][0]:
            for checkpoint in category["checkpoints"]:
                if "collection_cmd" in checkpoint:
                    try:
                        collection_cmds.append(
                            {
                                "category_name": category["name"],
                                "collection_cmd_type": checkpoint[
                                    "collection_cmd_type"
                                ],
                                "collection_cmd": checkpoint["collection_cmd"],
                            }
                        )
                    except KeyError as _err:
                        print(f"Error: {_err} is expected.", file=sys.stderr)
                    finally:
                        continue

        return ic(collection_cmds)

    def list_checks(self) -> List[Check]:
        """
        Returns the set of check commands of the checklist.
        """
        checks = []
        for category in self._checklist["categories"][0]:
            for checkpoint in category["checkpoints"]:
                if checkpoint["collect_only"] in ("true", "True"):
                    id = str(category["id"]) + "." + str(checkpoint["id"]) + ".1"
                    checks.append(self._create_empty_check(id))
                else:
                    for check in checkpoint["checks"]:
                        check["id"] = (
                            str(category["id"])
                            + "."
                            + str(checkpoint["id"])
                            + "."
                            + str(check["id"])
                        )
                        checks.append(Check(**check))
        return ic(checks)

    def get_json_reporting(self, results: List[CheckResult]) -> str:
        """
        Allows the generation of the exported JSON file for later use.
        """
        checklist = self._checklist
        for result in results:
            cat_id, checkpoint_id, check_id = (
                int(result.id.split(".")[0]),
                int(result.id.split(".")[1]),
                int(result.id.split(".")[2]),
            )
            result.id = check_id
            base = checklist["categories"][0][cat_id - 1]["checkpoints"][
                checkpoint_id - 1
            ]
            if isinstance(base, dict):
                if base["collect_only"] in ("true", "True"):
                    base["checks"] = [self._create_empty_check(1)]
                    continue

                checklist["categories"][0][cat_id - 1]["checkpoints"][
                    checkpoint_id - 1
                ]["checks"][check_id - 1] = result
            elif isinstance(base, Checkpoint):
                if base.collect_only in ("true", "True"):
                    base["checks"] = [self._create_empty_check(1)]
                    continue

                checklist["categories"][0][cat_id - 1]["checkpoints"][
                    checkpoint_id - 1
                ].checks[check_id - 1] = result
            else:
                continue

        return json.dumps(checklist, cls=ChecklistJsonEncoder, ensure_ascii=False)

    def remove_ignore_tag(self, json_data) -> str:
        """
        Remove ignore_tag used for translation before creating reports.
        """
        regex = r"\<\/?x\>"
        subst = ""
        json_data = json.loads(json_data)
        # for root in json_data:
        for category in json_data["categories"][0]:
            # name
            category["name"] = re.sub(
                regex,
                subst,
                category["name"],
                0,
                re.MULTILINE | re.IGNORECASE | re.DOTALL,
            )
            for checkpoint in category["checkpoints"]:
                # title
                checkpoint["title"] = re.sub(
                    regex,
                    subst,
                    checkpoint["title"],
                    0,
                    re.MULTILINE | re.IGNORECASE | re.DOTALL,
                )
                # description
                checkpoint["description"] = re.sub(
                    regex,
                    subst,
                    checkpoint["description"],
                    0,
                    re.MULTILINE | re.IGNORECASE | re.DOTALL,
                )
                for check in checkpoint["checks"]:
                    # title
                    check["title"] = re.sub(
                        regex,
                        subst,
                        check["title"],
                        0,
                        re.MULTILINE | re.IGNORECASE | re.DOTALL,
                    )
                    # description
                    check["description"] = re.sub(
                        regex,
                        subst,
                        check["description"],
                        0,
                        re.MULTILINE | re.IGNORECASE | re.DOTALL,
                    )
                    # recommendation_on_failed
                    check["recommendation_on_failed"] = re.sub(
                        regex,
                        subst,
                        check["recommendation_on_failed"],
                        0,
                        re.MULTILINE | re.IGNORECASE | re.DOTALL,
                    )
        return json.dumps(json_data, cls=ChecklistJsonEncoder, ensure_ascii=False)

    def get_original_format(self, checklist: List[Category]):
        """
        Takes content in the form of a category list and returns the same content in the original format
        """
        json_content = json.dumps(
            checklist, cls=ChecklistJsonEncoder, ensure_ascii=False
        )
        return yaml.dump(json.loads(json_content), sort_keys=False)
