#!/usr/bin/env python

from decorators import *
from icecream import ic
import os


@BashDecorator.decorator
def write_bash_script(content):
    return content


@BashDecoratorMAC.decorator
def write_bash_script_mac(content):
    return content


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
        for item in categories:
            checkpoints = item.checkpoints
            for checkpoint in range(len(checkpoints)):
                commands.append(checkpoints[checkpoint].collection)
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
                    [file.write(x + "\n") for x in content]
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
