from icecream import ic
from interactors.check_output import CheckOutputInteractor
from models import CheckResult
from pathlib import Path
from ports import IArchive, IChecklist
import inject
import os


class CheckArchiveInteractor:
    @inject.autoparams("checklist", "archive")
    def __init__(self, checklist: IChecklist, archive: IArchive) -> None:
        self._checklist = checklist
        self._archive = archive

    def execute(self, checklist, archive):
        self._checklist.parse_checklist(checklist)
        categories = self._checklist.get_categories()
        extract_path = self._archive.extract(archive)
        if extract_path is None:
            return

        results = []
        for root, dirs, files in os.walk(extract_path):
            check_result = []
            for file in files:
                filename = file.rsplit(".", 1)[0]
                check = self._checklist.get_check(categories, filename)
                with open(str(extract_path) + "/" + file, "r") as check_output:
                    content = ic(check_output.read())
                    check_result = {
                        "id": filename,
                        "description": check.description,
                        "type": check.type,
                        "cmd": check.cmd,
                        "expected": check.expected,
                        "verification_type": check.verification_type,
                        "recommandation_on_failed": check.recommandation_on_failed,
                        "cmd_output": content,
                        "see_also": check.see_also
                        if check.see_also is not None
                        else None,
                    }
                results.append(CheckResult(**check_result))
        return CheckOutputInteractor().execute(results)