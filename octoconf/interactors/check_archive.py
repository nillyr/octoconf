# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import os

import chardet
from icecream import ic
import inject

from octoconf.interactors.check_output import CheckOutputInteractor
from octoconf.models import CheckResult
from octoconf.ports import IArchive, IChecklist


class CheckArchiveInteractor:
    """
    Receives an archive with a certain extension (zip, tar.gz, other) and extracts the files in the "checks" folder. Each file corresponding to a particular check, a list of "CheckResult" objects is created and sent to the use case responsible for checking the results.
    """

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
        for _, _, files in os.walk(extract_path):
            check_result = []
            for file in files:
                filename = file.rsplit(".", 1)[0]
                check = self._checklist.get_check(categories, filename)
                if check is None:
                    continue
                with open(str(extract_path) + "/" + file, "rb") as check_output:
                    raw = check_output.read()
                    encoding = chardet.detect(raw)["encoding"]
                    if not encoding:
                        # This case can be seen when using the powershell Out-File cmdlet (utf8noBom)
                        encoding = "UTF-8-SIG"
                    content = raw.decode(encoding)

                    check_result = {
                        "id": filename,
                        "title": check.title,
                        "description": check.description
                        if check.description is not None
                        else None,
                        "type": check.type,
                        "cmd": check.cmd,
                        "expected": check.expected,
                        "verification_type": check.verification_type,
                        "cmd_output": content,
                        "severity": check.severity,
                        "recommendation_on_failed": check.recommendation_on_failed,
                        "see_also": check.see_also
                        if check.see_also is not None
                        else None,
                    }
                results.append(CheckResult(**check_result))
        return ic(results)
