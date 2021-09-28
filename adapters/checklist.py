#!/usr/bin/env python

import hjson
import json
from models import *
from ports.checklist import Checklist


class ChecklistAdapter(Checklist):
    def checklist_parser(self, filename):
        with open(filename, "r") as hjson_file:
            hson_checklist = hjson.loads(hjson_file.read())
            json_checklist = hjson.dumpsJSON(hson_checklist)
            checklist = json.loads(json_checklist)

        categories_list = []
        copyright = checklist[0]["copyright"]
        for item in checklist:
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

        return categories_list, copyright

    def get_commands(self, filename):
        categories, copyright = self.checklist_parser(filename)

        commands = []
        commands.append({"copyright": copyright})
        for category in categories:
            checks, lst = [], []
            checkpoints = category.checkpoints
            for checkpoint in range(len(checkpoints)):
                lst.append(checkpoints[checkpoint].collection)
                if checkpoints[checkpoint].performable == False:
                    continue
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

    def get_check(self, categories, cmd_id):
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
