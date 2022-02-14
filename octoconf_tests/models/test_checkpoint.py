# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoconf
# @since 1.0.0b

import sys

import pytest

sys.path.append("../octoconf/")
from octoconf.models.check import Check
from octoconf.models.checkpoint import Checkpoint


@pytest.fixture
def checks():
    checkA = Check(
        id="1",
        title="a_title",
        description="a_description",
        reference="a_reference",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        severity="a_severity",
        recommendation_on_failed="a_recommendation_on_failed",
        see_also="a_see_also",
    )

    checkB = Check(
        id="1",
        title="a_title",
        description="a_description",
        reference="a_reference",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        severity="a_severity",
        recommendation_on_failed="a_recommendation_on_failed",
        see_also="a_see_also",
    )

    checks = []
    checks.append(checkA)
    checks.append(checkB)

    return checks


def test_checkpoint_model_init(checks):
    a_checkpoint = Checkpoint(
        id="1",
        title="a_title",
        description="a_description",
        collection_cmd="a_collection_cmd",
        collection_cmd_type="a_collection_cmd_type",
        collect_only=False,
        checks=checks,
    )

    assert a_checkpoint.id == 1
    assert a_checkpoint.title == "a_title"
    assert a_checkpoint.description == "a_description"
    assert a_checkpoint.collection_cmd == "a_collection_cmd"
    assert a_checkpoint.collection_cmd_type == "a_collection_cmd_type"
    assert a_checkpoint.collect_only == False
    assert a_checkpoint.checks == checks