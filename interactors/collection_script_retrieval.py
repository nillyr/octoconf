#!/usr/bin/env python

from decorators import *
from icecream import ic
import os

newline = lambda x: "\n" if x in ("linux", "mac") else "\r\n"


class CollectionScriptRetrievalInteractor:
    __filename = lambda _, x, y: x if y == None else y

    def __init__(self, adapter):
        self.adapter = adapter

    def __write_checks_cmds(self, checksdir, content, cmds, pattern, platform):
        for category in content:
            for check_cmds in category["checks_cmds"]:
                output_file, cmd = check_cmds[0] + ".txt", check_cmds[1]
                if platform in ("linux", "mac"):
                    path = '"' + checksdir + '"/' + output_file + newline(platform)
                elif platform == "windows":
                    path = checksdir + "\\" + output_file + newline(platform)
                else:
                    continue
                cmds.append(ic(cmd + pattern + path))
        return cmds

    @BashDecorator.decorator
    def write_bash_script(self, content, platform, callback):
        cmds, str = ([], "")
        for i in range(len(content)):
            str += """
CATEGORY=\"{0}\"
echo "[*] Running {1} collection commands..."
/bin/mkdir -p {2}
""".format(
                content[i]["category_name"].replace(" ", "_"),
                '\\"${CATEGORY}\\"',
                '"${BASEDIR}"/"${CATEGORY}"/',
            )
            for cmd in content[i]["collection_cmds"]:
                str += cmd + newline(platform)
            cmds.append(str)
        return callback("${CHECKSDIR}", content, cmds, " > ", platform)

    @BashDecoratorMAC.decorator
    def write_bash_script_mac(self, content, platform, callback):
        cmds, str = ([], "")
        for i in range(len(content)):
            str += """
CATEGORY=\"{0}\"
echo "[*] Running {1} collection commands..."
/bin/mkdir -p {2}
""".format(
                content[i]["category_name"].replace(" ", "_"),
                '\\"${CATEGORY}\\"',
                '"${BASEDIR}"/"${CATEGORY}"/',
            )
            for cmd in content[i]["collection_cmds"]:
                str += cmd + newline(platform)
            cmds.append(str)
        return callback("${CHECKSDIR}", content, cmds, " > ", platform)

    @BatchDecorator.decorator
    def write_batch_script(self, content, platform, callback):
        cmds, str = ([], "")
        for i in range(len(content)):
            str += """
set category={0}
echo [*] Running {1} collection commands...
mkdir {2}
""".format(
                content[i]["category_name"].replace(" ", "_"),
                "%category%",
                "%basedir%\\%category%",
            )
            for cmd in content[i]["collection_cmds"]:
                str += cmd + newline(platform)
            cmds.append(str)
        return callback("%checksdir%", content, cmds, " > ", platform)

    @PowershellDecorator.decorator
    def write_powershell_script(self, content, platform, callback):
        cmds, str = ([], "")
        for i in range(len(content)):
            str += """
$category=\"{0}\"
Write-Output "[*] Running {1} collection commands..."
New-Item -ItemType directory -Path $basedir\\$category
""".format(
                content[i]["category_name"].replace(" ", "_"), "$category"
            )
            for cmd in content[i]["collection_cmds"]:
                str += cmd + newline(platform)
            cmds.append(str)
        return callback("$checksdir", content, cmds, " | Out-File -Path ", platform)

    def execute(self, args):
        commands, output, platform, language = (
            ic(self.adapter.get_commands(args["checklist"])),
            self.__filename(
                os.path.basename(os.path.splitext(args["checklist"])[0]), args["output"]
            ),
            args["platform"],
            args["language"],
        )

        with open(output, "w", newline=newline(platform)) as file:
            if platform in ("linux", "mac"):
                if language == "bash":
                    content = (
                        self.write_bash_script(
                            commands, platform, self.__write_checks_cmds
                        )
                        if platform == "linux"
                        else self.write_bash_script_mac(
                            commands, platform, self.__write_checks_cmds
                        )
                    )
                    [file.write(x) for x in content]
                    return 0
            elif platform == "windows":
                if language == "batch":
                    content = self.write_batch_script(
                        commands, platform, self.__write_checks_cmds
                    )
                    [file.write(x) for x in content]
                    return 0
                elif language == "powershell":
                    content = self.write_powershell_script(
                        commands, platform, self.__write_checks_cmds
                    )
                    [file.write(x) for x in content]
                    return 0
                else:
                    return 1
