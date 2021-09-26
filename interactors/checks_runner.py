#!/usr/bin/env python

from icecream import ic
from pathlib import Path
from platform import system
import asyncio
import datetime
import json
import re
import time


class ChecksRunnerInteractor:
    __timestamp = lambda _: datetime.datetime.fromtimestamp(time.time()).strftime(
        "%Y%m%d%H%M%S"
    )

    def __init__(self, adapter):
        self.adapter = adapter

    def __get_commands(self, categories):
        commands = []
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
        return ic(commands)

    async def run(self, cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return ic(stdout.decode("UTF-8"), stderr.decode("UTF-8"))

    def __preprocess_collection_cmd(self, basedir, category, cmd):
        if system() == "Windows" and "| Out-File -Path" in cmd:
            pattern = "| Out-File -Path"
            md = "New-Item -ItemType directory -Path "
        else:
            pattern = ">"
            md = "mkdir -p "

        output_file = re.split(pattern, cmd)[-1].strip()
        path = (
            Path.cwd()
            / basedir
            / category.replace(" ", "_")
            / Path(output_file).parent
        )
        if path.exists() == False:
            asyncio.run(self.run(md + str(path)))

        replace_path = path / Path(output_file).name
        return ic(re.split(pattern, cmd)[0] + pattern + " " + str(replace_path))

    def execute(self, basedir, checklist):
        categories = self.adapter.checklist_parser(checklist)
        cmds = self.__get_commands(categories)
        results = []
        for category in range(len(cmds)):
            collection_cmds = cmds[category]["collection_cmds"]
            [
                asyncio.run(
                    self.run(
                        self.__preprocess_collection_cmd(
                            basedir, cmds[category]["category_name"], collection_cmd
                        )
                    )
                )
                for collection_cmd in collection_cmds
            ]
            checks_cmds = cmds[category]["checks_cmds"]
            checks = []
            for checks_cmd in checks_cmds:
                checks.append(
                    {
                        "cmd_id": checks_cmd[0],
                        "cmd": checks_cmd[1],
                        "output": asyncio.run(self.run(checks_cmd[1])),
                    }
                )
            results.append(checks)

        path = Path.cwd() / basedir / self.__timestamp()
        with open(str(path) + "_checksrunner_results.json", "w") as json_file:
            json.dump(results, json_file)

        return results
