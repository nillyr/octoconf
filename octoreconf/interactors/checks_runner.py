# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from pathlib import Path
import platform
import re
from subprocess import Popen, PIPE, STDOUT, DEVNULL, TimeoutExpired
import sys

from icecream import ic
import inject

from octoreconf.interactors.check_output import CheckOutputInteractor
from octoreconf.models import CheckResult
from octoreconf.ports import IChecklist


class ChecksRunnerInteractor:
    """
    Use case allowing to execute the commands defined in the checklist provided as argument.
    """

    @inject.autoparams("checklist")
    def __init__(self, checklist: IChecklist) -> None:
        self._checklist = checklist

    def _run(self, cmd, cmd_type, is_check=False) -> str:
        """
        This method allows commands to be executed. The cmd_type argument is defined in the checklist.
        """
        if self._checklist.get_executable(cmd_type) == None or len(cmd) == 0:
            return ""

        shell = True
        if platform.system() == "Windows":
            shell = False
            cmd = [self._checklist.get_executable(cmd_type), cmd]

        stdout = str()

        # When the collection commands are run, the output is redirected to a file. No need to have it. On the other hand, when the checks are performed, stdout is needed
        proc = Popen(
            cmd,
            stdout=PIPE if is_check else DEVNULL,
            stderr=STDOUT,
            shell=shell,
        )
        try:
            # timeout: 3 min
            stdout, _ = ic(proc.communicate(timeout=180))
            return ic(str(stdout.decode("utf-8")))
        except AttributeError:
            # This case occurs when stdout is set to DEVNULL
            return ""
        except TimeoutExpired:
            proc.kill()
        except UnicodeDecodeError as _err:
            # This case happens when Windows is in French
            return ic(stdout.decode("cp1252"))
        except Exception as _err:
            print(f"Error: {_err}.", file=sys.stderr)

    def _preprocess_collection_cmd(self, basedir, category, cmd) -> str:
        """
        This method puts the audit proofs in the folder corresponding to the current category. Since the user is not aware of the folder automatically created during the tests, it is not possible to specify the exact path for the output of the files in the checklist.
        """
        regex_pattern = "\|\s*Out-File\s+-Encoding\s+utf8\s+(-(Append|FilePath)\s+)*|\s*>+\s*|\s*/(H|cfg)\s*"

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
                collection_cmd["collection_cmd_type"],
            )
            _ = self._run(
                self._preprocess_collection_cmd(output_directory, cat, cmd),
                cmd_type,
                False,
            )

        print("[*] Running checks...")
        checks = self._checklist.list_checks()
        results = []
        for check in checks:
            cmd_output = self._run(check.cmd, check.type, True)
            check_result = {
                "id": check.id,
                "description": check.description,
                "type": check.type,
                "cmd": check.cmd,
                "expected": check.expected,
                "verification_type": check.verification_type,
                "cmd_output": cmd_output,
                "severity": check.severity,
                "recommandation_on_failed": check.recommandation_on_failed,
                "see_also": check.see_also if check.see_also is not None else None,
            }

            results.append(CheckResult(**check_result))
        print("[+] Done")
        return CheckOutputInteractor().execute(ic(results))
