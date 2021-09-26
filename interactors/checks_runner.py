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
                if checkpoints[checkpoint].performable == False:
                    continue
                lst.append(checkpoints[checkpoint].collection)
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
                    "collection_cmds": lst,
                    "checks_cmds": checks,
                }
            )
        return ic(commands)

    async def run(self, cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        return ic(stdout.decode("UTF-8"))

    def __preprocess_collection_cmd(self, cmd):
        sys = system()
        if sys == "Windows":
            if ">" in cmd:
                output_file = cmd.split(">")[-1].strip()
                path = output_file[0 : -len(output_file.split("\\")[-1])]
                posix_path = Path(path)
                if posix_path.exists() == False:
                    asyncio.run(self.run("mkdir " + path))
                return cmd
            elif "| Out-File -Path" in cmd:
                output_file = re.split(r"Out-File -Path", cmd)[-1].strip()
                path = output_file[0 : -len(output_file.split("\\")[-1])]
                posix_path = Path(path)
                if posix_path.exists() == False:
                    asyncio.run(self.run("New-Item -ItemType directory -Path " + path))
                return cmd
        elif sys == "Linux" or sys == "Darwin":
            output_file = cmd.split(">")[-1].strip()
            path = output_file[0 : -len(output_file.split("/")[-1])]
            posix_path = Path(path)
            if posix_path.exists() == False:
                asyncio.run(self.run("mkdir -p " + path))
        else:
            return cmd

        return cmd

    def execute(self, checklist):
        categories = self.adapter.checklist_parser(checklist)
        cmds = self.__get_commands(categories)
        results = []
        for category in range(len(cmds)):
            collection_cmds = cmds[category]["collection_cmds"]
            [
                asyncio.run(self.run(self.__preprocess_collection_cmd(collection_cmd)))
                for collection_cmd in collection_cmds
            ]
            checks_cmds = cmds[category]["checks_cmds"]
            checks = []
            for checks_cmd in checks_cmds:
                checks.append(
                    {
                        "cmd_id": checks_cmd[0],
                        "cmd": checks_cmd[1],
                        "stdout": asyncio.run(self.run(checks_cmd[1])),
                    }
                )
            results.append(checks)

        with open(self.__timestamp() + "_checksrunner_results.json", "w") as json_file:
            json.dump(results, json_file)

        return results
