#!/usr/bin/env python

from decorators import *
from icecream import ic
import os


@BashDecorator.decorator
def write_bash_script(content):
    cmds, str = ([], "")
    for i in range(len(content)):
        str += """
SECTION=\"{0}\"
echo "[*] Running {1} collection commands..."
/bin/mkdir -p {2}
""".format(
            content[i]["category"],
            '\\"${SECTION}\\"',
            '"${BASEDIR}"/"${SECTION}"/',
        )
        for cmd in content[i]["collection_cmds"]:
            str += cmd + "\n"
        cmds.append(str)
    return cmds


@BashDecoratorMAC.decorator
def write_bash_script_mac(content):
    cmds, str = ([], "")
    for i in range(len(content)):
        str += """
SECTION=\"{0}\"
echo "[*] Running {1} collection commands..."
/bin/mkdir -p {2}
""".format(
            content[i]["category"],
            '\\"${SECTION}\\"',
            '"${BASEDIR}"/"${SECTION}"/',
        )
        for cmd in content[i]["collection_cmds"]:
            str += cmd + "\n"
        cmds.append(str)
    return cmds


@BatchDecorator.decorator
def write_batch_script(content):
    return content


@PowershellDecorator.decorator
def write_powershell_script(content):
    return content


class CollectionScriptRetrievalInteractor:
    __filename = lambda _, x, y: x if y == None else y

    def __init__(self, adapter):
        self.adapter = adapter

    def __get_commands(self, categories):
        commands = []
        for category in categories:
            lst = []
            ic(category.name)
            checkpoints = category.checkpoints
            for checkpoint in range(len(checkpoints)):
                lst.append(checkpoints[checkpoint].collection)
            commands.append({"category": category.name, "collection_cmds": lst})
        return ic(commands)

    def execute(self, args):
        categories, output, platform, language = (
            self.adapter.checklist_parser(args["checklist"]),
            self.__filename(
                os.path.basename(os.path.splitext(args["checklist"])[0]), args["output"]
            ),
            args["platform"],
            args["language"],
        )
        commands = self.__get_commands(categories)

        with open(output, "w") as file:
            if platform in ("linux", "mac"):
                if language == "bash":
                    content = (
                        write_bash_script(commands)
                        if platform == "linux"
                        else write_bash_script_mac(commands)
                    )
                    [file.write(x) for x in content]
                    return 0
            elif platform == "windows":
                if language == "batch":
                    content = write_batch_script(commands)
                    [file.write(x) for x in content]
                    return 0
                elif language == "powershell":
                    content = write_powershell_script(commands)
                    [file.write(x) for x in content]
                    return 0
                else:
                    return 1
