from icecream import ic

from decorators.script_generator import BatchDecorator
from ports.script_generator.windows_script import IWindowsScript


class WindowsBatchScript(IWindowsScript):
    """
    Class allowing the generation of the collection script for the indicated system.
    """

    def write_checks_cmds(self, checksdir, content, cmds):
        """
        Adds to the collection script all the check commands allowing the analysis of the results by this tool.
        """
        cmds.append(IWindowsScript._newline + "REM Checks" + IWindowsScript._newline)
        for category in content:
            for check_cmds in category["checks_cmds"]:
                output_file, cmd = check_cmds[0] + ".txt", check_cmds[1]
                if not cmd:
                    continue
                path = checksdir + "\\" + output_file + IWindowsScript._newline
                cmds.append(cmd + IWindowsScript._batch_pattern + path)
        return ic(cmds)

    @BatchDecorator.decorator
    def write_script(self, content, callback):
        """
        Adds to the collection script the set of commands for collecting proofs to perform manual verifications.
        """
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
                        "%basedir%\\%category%\\", cmd
                    )
                    + IWindowsScript._newline
                )
            cmds.append(str)
        return callback("%checksdir%", content, cmds)
