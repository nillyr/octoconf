# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from icecream import ic

from octoreconf.decorators.script_generator import PowershellDecorator
from octoreconf.ports.script_generator.windows_script import IWindowsScript


class WindowsPowershellScript(IWindowsScript):
    """
    Class allowing the generation of the collection script for the indicated system.
    """

    def write_checks_cmds(self, checksdir, content, cmds):
        """
        Adds to the collection script all the check commands allowing the analysis of the results by this tool.
        """
        cmds.append(IWindowsScript._newline + "# Checks" + IWindowsScript._newline)
        for category in content:
            for check_cmds in category["checks_cmds"]:
                output_file, cmd = check_cmds[0] + ".txt", check_cmds[1]
                if not cmd:
                    continue
                path = checksdir + "\\" + output_file + IWindowsScript._newline
                cmds.append(cmd + IWindowsScript._powershell_pattern + path)
        return ic(cmds)

    @PowershellDecorator.decorator
    def write_script(self, content, callback):
        """
        Adds to the collection script the set of commands for collecting proofs to perform manual verifications.
        """
        cmds, str = ([], "")
        for i in range(len(content)):
            str = """
$category=\"{0}\"
Write-Output "[*] Running {1} collection commands..."
New-Item -ItemType directory -Path $basedir\\$category
""".format(
                content[i]["category_name"].replace(" ", "_"), "$category"
            )
            for cmd in content[i]["collection_cmds"]:
                str += (
                    IWindowsScript.preprocess_collection_cmd(
                        "$basedir\\$category\\", cmd
                    )
                    + IWindowsScript._newline
                )
            cmds.append(str)
        return callback("$checksdir", content, cmds)
