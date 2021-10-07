import os
from pathlib import Path
import tarfile
import zipfile

from icecream import ic

from ports.archive import IArchive


class ArchiveAdapter(IArchive):
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
            if "checks" in os.path.splitext(tarinfo.name)[0]:
                yield tarinfo

    def extract(self, archive) -> Path:
        """
        Performs archive extraction.
        To date, only zip and tar.gz archives are supported.
        """
        path = Path(archive)
        if not path.exists():
            return

        while path != path.with_suffix(""):
            path = path.with_suffix("")

        if tarfile.is_tarfile(archive):
            tar = tarfile.open(archive)
            tar.extractall(path, members=self.checks_files_only(tar))
            tar.close()
        elif zipfile.is_zipfile(archive):
            with zipfile.ZipFile(archive, "r") as zip_file:
                files = zip_file.namelist()
                for file in files:
                    if "checks" in file:
                        zip_file.extract(file, path)
            zip_file.close()
        else:
            pass

        for root, dirs, files in os.walk(path):
            if "checks" in root:
                path = Path(root)

        return ic(path)
