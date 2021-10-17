from pathlib import Path

import inject
import pytest

from adapters import CheckerAdapter, ChecklistAdapter
from components.report_generators.xlsx_report_generator import (
    IReportGenerator,
    XlsxGenerator,
)
from interactors.checks_runner import ChecksRunnerInteractor
from ports import IChecker, IChecklist
from utils import *


@pytest.fixture
def setup():
    inject.clear_and_configure(
        lambda binder: binder.bind(IChecker, CheckerAdapter())
        .bind(IChecklist, ChecklistAdapter())
        .bind(IReportGenerator, XlsxGenerator())
    )
    global_values.set_localize("en")
    yield None
    inject.clear()


@pytest.fixture
def unix_checklist_path():
    return "tests/interactors/checklists/unix/test_1.hjson"


@pytest.fixture
def checklist_path(unix_checklist_path):
    return unix_checklist_path


@pytest.fixture
def output_path():
    return "tests/.ignore/pytest/"


def test_checks_runner_file_creation(setup, checklist_path, output_path):
    """
    This test alone verifies that the spaces in the category title have been substituted and that the output path has been modified without error. It also allows you to check that the command (cmd + pattern + path + file) has been carried out correctly.
    """
    uc = ChecksRunnerInteractor()
    uc.execute(checklist_path, output_path)

    assert Path(output_path + "a_category_with_some_spaces/whoami.txt").exists()