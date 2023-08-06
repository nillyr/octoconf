# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
from pathlib import Path

import chardet
import inject

from octoconf.interfaces.archive import IArchive
from octoconf.interfaces.baseline import IBaseline
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class CheckArchiveUseCase:
    """
    Receives an archive with a certain extension (zip, tar.gz, other) and extracts the files in the "checks" folder. Each file corresponding to a particular check, a list of "CheckResult" objects is created and sent to the use case responsible for checking the results.
    """

    @inject.autoparams("adapter", "archive")
    def __init__(self, adapter: IBaseline, archive: IArchive) -> None:
        self._adapter = adapter
        self._archive = archive

    def execute(self, baseline_path: str, archive_path: str) -> list:
        logger.info(f"Running archive analysis use case")
        logger.debug(
            f"Running with the following arguments: archive = {archive_path}, baseline = {baseline_path}"
        )

        baseline = self._adapter.load_baseline_from_file(Path(baseline_path))
        if baseline is None:
            return []

        extract_path = self._archive.extract(archive_path)
        if extract_path is None:
            return []

        results = []
        for file in extract_path.glob("**/*.txt"):
            rule = self._adapter.get_check(baseline, file.name.rsplit(".", 1)[0])
            if rule is None:
                continue
            with open(str(file), "rb") as check_output:
                raw = check_output.read()
                encoding = chardet.detect(raw)["encoding"]
                if not encoding:
                    # True when using the pwsh Out-File cmdlet (utf8noBom)
                    encoding = "UTF-8-SIG"
                results.append(
                    self._adapter.update_rule_with_output_result(
                        rule, raw.decode(encoding)
                    )
                )
        return results
