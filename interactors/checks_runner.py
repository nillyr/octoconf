from icecream import ic
from interactors.check_output import CheckOutputInteractor
from models import CheckResult
from pathlib import Path
from platform import system
from ports import IChecklist
import asyncio
import inject
import re


class ChecksRunnerInteractor:
    @inject.autoparams("checklist")
    def __init__(self, checklist: IChecklist) -> None:
        self._checklist = checklist

    async def _run(self, cmd, cmd_type) -> str:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            executable=self._checklist.get_executable(cmd_type),
        )
        stdout, _ = await proc.communicate()
        return ic(stdout.decode("UTF-8"))

    def _preprocess_collection_cmd(self, basedir, category, cmd) -> str:
        if system() == "Windows" and "| Out-File -Path" in cmd:
            pattern = "| Out-File -Path"
        else:
            pattern = ">"

        output_file = re.split(pattern, cmd)[-1].strip()
        path = (
            Path.cwd() / basedir / category.replace(" ", "_") / Path(output_file).parent
        )
        path.mkdir(parents=True, exist_ok=True)
        replace_path = path / Path(output_file).name
        return ic(re.split(pattern, cmd)[0] + pattern + " " + str(replace_path))

    def execute(self, checklist, output_directory):
        self._checklist.parse_checklist(checklist)
        collection_cmds = self._checklist.list_collection_cmds()
        for collection_cmd in collection_cmds:
            cat, cmd, cmd_type = (
                collection_cmd["category_name"],
                collection_cmd["collection_cmd"],
                collection_cmd["collection_cmd_type"],
            )
            asyncio.run(
                self._run(
                    self._preprocess_collection_cmd(output_directory, cat, cmd),
                    cmd_type,
                )
            )

        checks = self._checklist.list_checks()
        results = []
        for check in checks:
            cmd_output = asyncio.run(self._run(check.cmd, check.type))
            check_result = {
                "id": check.id,
                "description": check.description,
                "type": check.type,
                "cmd": check.cmd,
                "expected": check.expected,
                "verification_type": check.verification_type,
                "recommandation_on_failed": check.recommandation_on_failed,
                "cmd_output": cmd_output,
                "see_also": check.see_also if check.see_also is not None else None,
            }

            results.append(CheckResult(**check_result))
        return CheckOutputInteractor().execute(ic(results))
