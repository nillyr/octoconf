# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
from pathlib import Path
import tarfile
from typing import Generator, Optional
import zipfile

from octoconf.interfaces.archive import IArchive
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class ArchiveInterfaceAdapter(IArchive):
    _results_dir = "10_octoconf_checks"

    def __init__(self) -> None:
        pass

    def checks_files_only(self, members) -> Generator:
        for tarinfo in members:
            if self._results_dir in str(Path(tarinfo.name).parent).lower():
                yield tarinfo

    def extract(self, archive) -> Optional[Path]:
        path = Path(archive)
        if not path.exists():
            return None

        if path.stem == self._results_dir:
            # Archive already extracted
            return path

        # Where to extract files
        path = path.parent

        logger.debug(f"Extracting archive {archive} into {path}")

        try:
            if tarfile.is_tarfile(archive):
                tar = tarfile.open(archive)
                tar.extractall(path, members=self.checks_files_only(tar))
                tar.close()
            elif zipfile.is_zipfile(archive):
                with zipfile.ZipFile(archive, "r") as zip_file:
                    files = zip_file.namelist()
                    for file in files:
                        if self._results_dir in file.lower():
                            zip_file.extract(file, path)
                zip_file.close()
            else:
                return None
        except:
            logger.exception("Unable to extract archive")
            return None

        return path / self._results_dir
