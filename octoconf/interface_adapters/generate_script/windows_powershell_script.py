# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import re

from icecream import ic

from octoconf.decorators.generate_script.powershell_decorator import PowershellDecorator
from octoconf.interfaces.generate_script.windows_script import IWindowsScript


class WindowsPowershellScript(IWindowsScript):
    """
    Class allowing the generation of the collection script for the indicated system.
    """

    def write_checks_cmds(self, checksdir, content, cmds):
        """
        Adds to the collection script all the check commands allowing the analysis of the results by this tool.
        """
        cmds.append(
            IWindowsScript._newline
            + 'Write-Output "[*] Starting compliance checks..."'
            + IWindowsScript._newline
        )
        for category in content:
            for commands in category["commands"]:
                output_file, check_cmd = (
                    commands["rule"] + ".txt",
                    commands["check"].rstrip(),
                )
                if not check_cmd:
                    continue
                path = checksdir + "\\" + output_file + IWindowsScript._newline
                cmds.append(check_cmd + IWindowsScript._powershell_pattern + path + IWindowsScript._newline)
        cmds.append(
            'Write-Output "[+] Finished compliance checks."'
            + IWindowsScript._newline
        )
        return ic(cmds)

    @PowershellDecorator.decorator
    def write_script(self, utils_content, content, callback):
        """
        Adds to the collection script the set of commands for collecting proofs to perform manual verifications.
        """
        cmds, str = ([], "")
        regex = r"(</?x>)|[^a-zàâçéèêëîïôûù0-9\-]"

        cmds.append(IWindowsScript._newline + utils_content)
        for category in content:
            str = """
$category=\"{0}\"
Write-Output "[*] Starting collection commands of category: {1}..."
New-Item -ItemType Directory -Force -Path $basedir\\$category | Out-Null
""".format(
                re.sub(
                    regex,
                    "_",
                    category["category"],
                    0,
                    re.IGNORECASE,
                ),
                "$category",
            )
            for cmd in category["commands"]:
                str += (
                    IWindowsScript.preprocess_collection_cmd(
                        "$basedir\\$category\\", cmd["collection_cmd"]
                    )
                    + IWindowsScript._newline
                )
            cmds.append(str)
            cmds.append(
                """Write-Output "[+] Finished collection commands of category: {0}."
""".format(
                    "$category",
                )
            )
        return callback("$checksdir", content, cmds)
