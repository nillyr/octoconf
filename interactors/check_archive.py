#!/usr/bin/env python

from icecream import ic
from pathlib import Path
import datetime
import json
import os
import tarfile
import time
import zipfile


class CheckArchiveInteractor:
    __timestamp = lambda _: datetime.datetime.fromtimestamp(time.time()).strftime(
        "%Y%m%d%H%M%S"
    )

    def __init__(self, adapter):
        self.adapter = adapter

    def __checks_files_only(self, members):
        for tarinfo in members:
            if "checks" in os.path.splitext(tarinfo.name)[0]:
                yield tarinfo

    def __extract(self, archive):
        path = Path(archive)
        if not path.exists():
            return

        while path != path.with_suffix(""):
            path = path.with_suffix("")

        if tarfile.is_tarfile(archive):
            tar = tarfile.open(archive)
            tar.extractall(path, members=self.__checks_files_only(tar))
            tar.close()
        elif zipfile.is_zipfile(archive):
            with zipfile.ZipFile(archive, "r") as zip_file:
                files = ic(zip_file.namelist())
                for file in files:
                    if "checks" in file:
                        zip_file.extract(file, path)
            zip_file.close()
        else:
            pass

        for root, dirs, files in os.walk(path):
            if "checks" in root:
                path = Path(root)

        return path

    def execute(self, basedir, archive, checklist):
        categories = self.adapter.checklist_parser(checklist)
        extract_path = ic(self.__extract(archive))
        if extract_path is None:
            return

        results = []
        for root, dirs, files in os.walk(extract_path):
            checks = []
            for file in files:
                cmd_id = file.rsplit(".", 1)[0]
                with open(str(extract_path) + "/" + file, "r") as check_output:
                    content = ic(check_output.read())
                checks.append(
                    {
                        "cmd_id": cmd_id,
                        "cmd": self.adapter.get_check(categories, cmd_id).cmd,
                        "output": (content, ""),
                    }
                )
        results.append(checks)
        path = Path.cwd() / basedir / self.__timestamp()
        with open(str(path) + "_checkarchive_results.json", "w") as json_file:
            json.dump(results, json_file)

        return ic(results)
