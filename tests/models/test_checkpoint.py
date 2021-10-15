import pytest

from models.check import Check
from models.checkpoint import Checkpoint


@pytest.fixture
def checks():
    checkA = Check(
        id="1",
        description="a_description",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        recommandation_on_failed="a_recommandation_on_failed",
        see_also="a_see_also",
    )

    checkB = Check(
        id="1",
        description="a_description",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        recommandation_on_failed="a_recommandation_on_failed",
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
        reference="a_reference",
        collection_cmd="a_collection_cmd",
        collection_cmd_type="a_collection_cmd_type",
        checks=checks,
    )

    assert a_checkpoint.id == 1
    assert a_checkpoint.title == "a_title"
    assert a_checkpoint.description == "a_description"
    assert a_checkpoint.reference == "a_reference"
    assert a_checkpoint.collection_cmd == "a_collection_cmd"
    assert a_checkpoint.collection_cmd_type == "a_collection_cmd_type"
    assert a_checkpoint.checks == checks
