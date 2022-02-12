# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from pathlib import Path
import sys

import inject
import pytest

sys.path.append("../octoreconf/")
from octoreconf.adapters import CheckerAdapter, ChecklistAdapter, CommandRunnerFactory
from octoreconf.adapters.report_generator import ReportGeneratorAdapter
from octoreconf.interactors.checks_runner import ChecksRunnerInteractor
from octoreconf.ports import (
    IChecker,
    IChecklist,
    ICommandRunnerFactory,
    IReportGenerator,
)
from octoreconf.utils import *


@pytest.fixture
def setup():
    inject.clear_and_configure(
        lambda binder: binder.bind(IChecker, CheckerAdapter())
        .bind(IChecklist, ChecklistAdapter())
        .bind(ICommandRunnerFactory, CommandRunnerFactory())
        .bind(IReportGenerator, ReportGeneratorAdapter())
    )
    global_values.set_localize("en")
    yield None
    inject.clear()


@pytest.fixture
def unix_checklist_path():
    return "octoreconf_tests/interactors/checklists/unix/test.yaml"


@pytest.fixture
def checklist_path(unix_checklist_path):
    return unix_checklist_path


@pytest.fixture
def output_path():
    return "octoreconf_tests/.ignore/pytest/"


def test_checks_runner_file_creation(setup, checklist_path, output_path):
    """
    This test alone verifies that the spaces in the category title have been substituted and that the output path has been modified without error. It also allows you to check that the command (cmd + pattern + path + file) has been carried out correctly.
    """
    uc = ChecksRunnerInteractor()
    uc.execute(checklist_path, output_path)

    assert Path(output_path + "pytest_category/whoami.txt").exists()
