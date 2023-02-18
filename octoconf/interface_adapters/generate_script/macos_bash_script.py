# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import re

from icecream import ic

from octoconf.decorators.generate_script import BashDecoratorMAC
from octoconf.interfaces.generate_script.unix_script import IUnixScript


class MacOSBashScript(IUnixScript):
    """
    Class allowing the generation of the collection script for the indicated system.
    """

    def write_checks_cmds(self, checksdir, content, cmds):
        """
        Adds to the collection script all the check commands allowing the analysis of the results by this tool.
        """
        cmds.append(IUnixScript._newline + "# Checks" + IUnixScript._newline)
        cmds.append(IUnixScript._newline
            + "echo \"[*] Running Checks ...\""
            + IUnixScript._newline)
        for category in content:
            for commands in category["commands"]:
                output_file, cmd = commands["rule"] + ".txt", commands["check"].rstrip()
                if not cmd:
                    continue
                path = '"' + checksdir + '"/' + output_file + IUnixScript._newline
                cmds.append(cmd + IUnixScript._pattern + path)
        return ic(cmds)

    @BashDecoratorMAC.decorator
    def write_script(self, utils_content, content, callback):
        """
        Adds to the collection script the set of commands for collecting proofs to perform manual verifications.
        """
        cmds, str = ([], "")
        regex = r"(</?x>)|[^a-zàâçéèêëîïôûù0-9\-]"

        cmds.append(IUnixScript._newline + utils_content)
        for category in content:
            str = """
CATEGORY=\"{0}\"
echo "[*] Running {1} collection commands..."
mkdir -p {2}
""".format(
                re.sub(
                    regex,
                    "_",
                    category["category"],
                    0,
                    re.IGNORECASE,
                ),
                '\\"${CATEGORY}\\"',
                '"${BASEDIR}"/"${CATEGORY}"/',
            )
            for cmd in category["commands"]:
                str += (
                    IUnixScript.preprocess_collection_cmd(
                        '"${BASEDIR}"/"${CATEGORY}"/', cmd["collection_cmd"]
                    )
                    + IUnixScript._newline
                )
            cmds.append(str)
        return callback("${CHECKSDIR}", content, cmds)
