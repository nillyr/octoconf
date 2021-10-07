from enum import Enum
import hjson
import json
from typing import List
import sys

from icecream import ic

from components.json_encoders.checklist import ChecklistJsonEncoder
from models import *
from ports.checklist import IChecklist


class NoValue(Enum):
    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)


class ChecklistAdapter(IChecklist):
    _instance = None
    _checklist = None

    class CmdType(NoValue):
        # WINDOWS
        AUDIT_POWERSHELL = "powershell.exe"
        BATCH_EXEC = "cmd.exe"
        # UNIX
        CMD_EXEC = "/bin/bash"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IChecklist, cls).__new__(cls)
        return cls._instance

    def parse_checklist(self, checklist) -> None:
        if self._checklist is None:
            with open(checklist, "r") as hjson_file:
                hson_checklist = hjson.loads(hjson_file.read())
                json_checklist = hjson.dumpsJSON(hson_checklist)
                self._checklist = json.loads(json_checklist)

    def get_executable(self, cmd_type) -> str:
        if cmd_type == "AUDIT_POWERSHELL":
            return self.CmdType.AUDIT_POWERSHELL.value
        if cmd_type == "BATCH_EXEC":
            return self.CmdType.BATCH_EXEC.value
        if cmd_type == "CMD_EXEC":
            return self.CmdType.CMD_EXEC.value
        return

    def get_categories(self) -> List[Category]:
        categories_list = []
        for item in self._checklist:
            categories_list = []
            for category in item["categories"]:
                checkpoints_list = []
                for checkpoint in category["checkpoints"]:
                    checks_list = []
                    for check in checkpoint["checks"]:
                        checks_list.append(Check(**check))
                    checkpoint["checks"] = checks_list
                    checkpoints_list.append(Checkpoint(**checkpoint))
                category["checkpoints"] = checkpoints_list
                categories_list.append(Category(**category))

        return categories_list

    def get_commands(self):
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
        category_id, checkpoint_id, check_id = (
            int(cmd_id.split(".")[0]),
            int(cmd_id.split(".")[1]),
            int(cmd_id.split(".")[2]),
        )
        check = (
            categories[category_id - 1]
            .checkpoints[checkpoint_id - 1]
            .checks[check_id - 1]
        )
        return check

    def list_collection_cmds(self):
        collection_cmds = []
        for item in self._checklist:
            for category in item["categories"]:
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
        checks = []
        for item in self._checklist:
            for category in item["categories"]:
                for checkpoint in category["checkpoints"]:
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
        checklist = self._checklist
        for result in results:
            cat_id, checkpoint_id, check_id = (
                int(result.id.split(".")[0]),
                int(result.id.split(".")[1]),
                int(result.id.split(".")[2]),
            )
            result.id = check_id
            base = checklist[0]["categories"][cat_id - 1]["checkpoints"][
                checkpoint_id - 1
            ]
            if isinstance(base, dict):
                checklist[0]["categories"][cat_id - 1]["checkpoints"][
                    checkpoint_id - 1
                ]["checks"][check_id - 1] = result
            elif isinstance(base, Checkpoint):
                checklist[0]["categories"][cat_id - 1]["checkpoints"][
                    checkpoint_id - 1
                ].checks[check_id - 1] = result
            else:
                continue

        return json.dumps(checklist, cls=ChecklistJsonEncoder, ensure_ascii=False)
