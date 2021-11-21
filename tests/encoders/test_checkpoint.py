# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json
import sys

import pytest

sys.path.append("../octoreconf/")
from octoreconf.components.json_encoders.checkpoint import CheckpointJsonEncoder
from octoreconf.models.check import Check
from octoreconf.models.checkpoint import Checkpoint


@pytest.fixture
def checks():
    return [
        Check(
            id="1",
            title="a_title",
            description="a_description",
            type="a_type",
            cmd="a_cmd",
            expected="a_expected",
            verification_type="a_verification_type",
            severity="a_severity",
            recommendation_on_failed="a_recommendation_on_failed",
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
        collect_only=False,
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
        "collect_only": false,
        "checks": [{{
            "id": "1",
            "title": "a_title",
            "description": "a_description",
            "type": "a_type",
            "cmd": "a_cmd",
            "expected": "a_expected",
            "verification_type": "a_verification_type",
            "cmd_output": "",
            "result": "",
            "severity": "a_severity",
            "recommendation_on_failed": "a_recommendation_on_failed",
            "see_also": "a_see_also"
        }}]
    }}
    """

    json_checkpoint = json.dumps(a_checkpoint, cls=CheckpointJsonEncoder)
    assert json.loads(json_checkpoint) == json.loads(expected_json)
