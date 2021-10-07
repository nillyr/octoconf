from icecream import ic

from decorators.script_generator import BashDecoratorMAC
from ports.script_generator.unix_script import IUnixScript


class MacOSBashScript(IUnixScript):
    def write_checks_cmds(self, checksdir, content, cmds):
        cmds.append(IUnixScript._newline + "# Checks" + IUnixScript._newline)
        for category in content:
            for check_cmds in category["checks_cmds"]:
                output_file, cmd = check_cmds[0] + ".txt", check_cmds[1]
                path = '"' + checksdir + '"/' + output_file + IUnixScript._newline
                cmds.append(cmd + IUnixScript._pattern + path)
        return ic(cmds)

    @BashDecoratorMAC.decorator
    def write_script(self, content, callback):
        cmds, str = ([], "")
        for i in range(len(content)):
            str = """
CATEGORY=\"{0}\"
echo "[*] Running {1} collection commands..."
/bin/mkdir -p {2}
""".format(
                content[i]["category_name"].replace(" ", "_"),
                '\\"${CATEGORY}\\"',
                '"${BASEDIR}"/"${CATEGORY}"/',
            )
            for cmd in content[i]["collection_cmds"]:
                str += (
                    IUnixScript.preprocess_collection_cmd(
                        '"${BASEDIR}"/"${CATEGORY}"/', cmd
                    )
                    + IUnixScript._newline
                )
            cmds.append(str)
        return callback("${CHECKSDIR}", content, cmds)
