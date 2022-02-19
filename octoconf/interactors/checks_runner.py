# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from pathlib import Path
import platform
import re

from icecream import ic
import inject

from octoconf.adapters.redirector_regex.redirector_regex import RedirectorRegex
from octoconf.interactors.check_output import CheckOutputInteractor
from octoconf.models import CheckResult
from octoconf.ports import IChecklist
from octoconf.ports.runner.command_runner_abstract_factory import (
    ICommandRunnerFactory,
)


class ChecksRunnerInteractor:
    """
    Use case allowing to execute the commands defined in the checklist provided as argument.
    """

    @inject.autoparams("checklist", "factory")
    def __init__(self, checklist: IChecklist, factory: ICommandRunnerFactory) -> None:
        self._checklist = checklist
        self._runner = factory.get_runner()

    def _preprocess_collection_cmd(self, basedir, category, cmd) -> str:
        """
        This method puts the audit proofs in the folder corresponding to the current category. Since the user is not aware of the folder automatically created during the tests, it is not possible to specify the exact path for the output of the files in the checklist.
        """
        # Remove ignore tag in category
        regex = r"\<\/?x\>"
        subst = ""
        category = re.sub(
            regex, subst, category, 0, re.MULTILINE | re.IGNORECASE | re.DOTALL
        )

        regex_pattern = RedirectorRegex.get_redirector_regex(platform.system())

        output_file = re.split(regex_pattern, cmd)[-1].strip()
        path = (
            Path.cwd() / basedir / category.replace(" ", "_") / Path(output_file).parent
        )
        path.mkdir(parents=True, exist_ok=True)
        replace_path = path / Path(output_file).name
        return ic(
            re.split(regex_pattern, cmd)[0]
            + re.search(regex_pattern, cmd).group(0)
            + str(replace_path)
        )

    def execute(self, checklist, output_directory):
        """
        Execute all the commands and for each check, create an object of type "CheckResult". These are returned as a list to check the results with the expected results.
        """
        print("[*] Running collection commands (this may take a while)...")
        self._checklist.parse_checklist(checklist)
        collection_cmds = self._checklist.list_collection_cmds()
        for collection_cmd in collection_cmds:
            cat, cmd, cmd_type = (
                collection_cmd["category_name"],
                collection_cmd["collection_cmd"],
                self._checklist.get_executable(collection_cmd["collection_cmd_type"]),
            )
            if cmd_type is None or len(cmd) == 0:
                continue

            _ = self._runner.exec(
                self._preprocess_collection_cmd(output_directory, cat, cmd),
                cmd_type,
            )

        print("[*] Running checks...")
        checks = self._checklist.list_checks()
        results = []
        for check in checks:
            cmd_type = self._checklist.get_executable(check.type)
            if cmd_type is None or len(check.cmd) == 0:
                cmd_output = ""
            else:
                cmd_output = self._runner.exec(check.cmd, cmd_type, True)
            check_result = {
                "id": check.id,
                "title": check.title,
                "description": check.description
                if check.description is not None
                else None,
                "type": check.type,
                "cmd": check.cmd,
                "expected": check.expected,
                "verification_type": check.verification_type,
                "cmd_output": cmd_output if cmd_output is not None else "",
                "severity": check.severity,
                "recommendation_on_failed": check.recommendation_on_failed,
                "see_also": check.see_also if check.see_also is not None else None,
            }

            results.append(CheckResult(**check_result))
        print("[+] Done")
        return CheckOutputInteractor().execute(ic(results))
