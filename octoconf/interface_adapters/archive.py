# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
from pathlib import Path
import tarfile
import zipfile

from octoconf.interfaces.archive import IArchive
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class ArchiveInterfaceAdapter(IArchive):
    """
    Class allowing to manipulate the archives containing the results of the collection script.
    """

    def __init__(self) -> None:
        pass

    def checks_files_only(self, members):
        """
        Generator method indicating the files to be extracted only (for tar.gz archives).
        """
        for tarinfo in members:
            if "10_octoconf_checks" in str(Path(tarinfo.name).parent).lower():
                yield tarinfo

    def extract(self, archive) -> Path:
        """
        Performs archive extraction.
        To date, only zip and tar.gz archives are supported.
        """
        path = Path(archive)
        if not path.exists():
            return

        # where to extract files
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
                        if "10_octoconf_checks" in file.lower():
                            zip_file.extract(file, path)
                zip_file.close()
            else:
                pass
        except:
            logger.exception("Unable to extract archive")
            pass

        return path / "10_octoconf_checks"
