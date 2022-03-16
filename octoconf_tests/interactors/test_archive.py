# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

import pytest

sys.path.append("../octoconf/")
from octoconf.adapters.archive import ArchiveAdapter


@pytest.fixture
def tar_gz_archive():
    return "octoconf_tests/interactors/archive/tryme.tar.gz"


@pytest.fixture
def zip_archive():
    return "octoconf_tests/interactors/archive/tryme.zip"


def test_extract_checks_files_only_from_nothing():
    a_path = ArchiveAdapter().extract("null")
    assert a_path is None


def test_extract_checks_files_only_from_tar_gz(tar_gz_archive):
    a_path = ArchiveAdapter().extract(tar_gz_archive)
    extracted = []
    for file in a_path.glob("**/*.txt"):
        extracted.append(str(file.name))

    assert "1.1.1.txt" in extracted
    assert "1.1.2.txt" in extracted


def test_extract_checks_files_only_from_zip(zip_archive):
    a_path = ArchiveAdapter().extract(zip_archive)
    extracted = []
    for file in a_path.glob("**/*.txt"):
        extracted.append(str(file.name))

    assert "1.1.1.txt" in extracted
    assert "1.1.2.txt" in extracted
