from decorators.script_generator import BatchDecorator
from icecream import ic
from ports.script_generator.windows_script import IWindowsScript


class WindowsBatchScript(IWindowsScript):
    def write_checks_cmds(self, checksdir, content, cmds):
        cmds.append(IWindowsScript._newline + "REM Checks" + IWindowsScript._newline)
        for category in content:
            for check_cmds in category["checks_cmds"]:
                output_file, cmd = check_cmds[0] + ".txt", check_cmds[1]
                path = checksdir + "\\" + output_file + IWindowsScript._newline
                cmds.append(ic(cmd + IWindowsScript._batch_pattern + path))
        return cmds

    @BatchDecorator.decorator
    def write_script(self, content, callback):
        cmds, str = ([], "")
        for i in range(len(content)):
            str = """
set category={0}
echo [*] Running {1} collection commands...
mkdir {2}
""".format(
                content[i]["category_name"].replace(" ", "_"),
                "%category%",
                "%basedir%\\%category%",
            )
            for cmd in content[i]["collection_cmds"]:
                str += (
                    IWindowsScript.preprocess_collection_cmd(
                        "%basedir%\\%category%\\", cmd, IWindowsScript._batch_pattern
                    )
                    + IWindowsScript._newline
                )
            cmds.append(str)
        return callback("%checksdir%", content, cmds)
