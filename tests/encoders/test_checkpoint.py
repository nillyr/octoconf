import json

import pytest

from components.json_encoders.checkpoint import CheckpointJsonEncoder
from models.check import Check
from models.checkpoint import Checkpoint


@pytest.fixture
def checks():
    return [
        Check(
            id="1",
            description="a_description",
            type="a_type",
            cmd="a_cmd",
            expected="a_expected",
            verification_type="a_verification_type",
            recommandation_on_failed="a_recommandation_on_failed",
            see_also="a_see_also",
        )
    ]


def test_serialize_checkpoint(checks):
    a_checkpoint = Checkpoint(
        id=1,
        title="a_title",
        description="a_description",
        reference="a_reference",
        collection_cmd="a_collection_cmd",
        collection_cmd_type="a_collection_cmd_type",
        checks=checks,
    )

    expected_json = f"""
    {{
        "id": 1,
        "title": "a_title",
        "description": "a_description",
        "reference": "a_reference",
        "collection_cmd": "a_collection_cmd",
        "collection_cmd_type": "a_collection_cmd_type",
        "checks": [{{
            "id": "1",
            "description": "a_description",
            "type": "a_type",
            "cmd": "a_cmd",
            "expected": "a_expected",
            "verification_type": "a_verification_type",
            "cmd_output": "",
            "result": "",
            "recommandation_on_failed": "a_recommandation_on_failed",
            "see_also": "a_see_also"
        }}]
    }}
    """

    json_checkpoint = json.dumps(a_checkpoint, cls=CheckpointJsonEncoder)
    assert json.loads(json_checkpoint) == json.loads(expected_json)
