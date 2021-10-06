from decorators.script_generator import PowershellDecorator
from icecream import ic
from ports.script_generator.windows_script import IWindowsScript


class WindowsPowershellScript(IWindowsScript):
    def write_checks_cmds(self, checksdir, content, cmds):
        cmds.append(IWindowsScript._newline + "# Checks" + IWindowsScript._newline)
        for category in content:
            for check_cmds in category["checks_cmds"]:
                output_file, cmd = check_cmds[0] + ".txt", check_cmds[1]
                path = checksdir + "\\" + output_file + IWindowsScript._newline
                cmds.append(cmd + IWindowsScript._powershell_pattern + path)
        return ic(cmds)

    @PowershellDecorator.decorator
    def write_script(self, content, callback):
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
                        "$basedir\\$category\\", cmd, IWindowsScript._powershell_pattern
                    )
                    + IWindowsScript._newline
                )
            cmds.append(str)
        return callback("$checksdir", content, cmds)
