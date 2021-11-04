# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json

import pytest

from components.json_encoders.checklist import ChecklistJsonEncoder
from models import *


@pytest.fixture
def check_result():
    return [
        CheckResult(
            id="1",
            description="a_description",
            type="a_type",
            cmd="a_cmd",
            expected="a_expected",
            verification_type="a_verification_type",
            cmd_output="a_cmd_output",
            result=True,
            severity="a_severity",
            recommandation_on_failed="a_recommandation_on_failed",
            see_also="a_see_also",
        )
    ]


@pytest.fixture
def checkpoints(check_result):
    return [
        Checkpoint(
            id=1,
            title="a_title",
            description="a_description",
            reference="a_reference",
            collection_cmd="a_collection_cmd",
            collection_cmd_type="a_collection_cmd_type",
            collect_only=False,
            checks=check_result,
        )
    ]


def test_serialize_category(checkpoints):
    a_category = Category(
        id=1,
        name="a_name",
        checkpoints=checkpoints,
    )

    expected_json = f"""
    {{
        "id": 1,
        "name": "a_name",
        "checkpoints": [{{
            "id": 1,
            "title": "a_title",
            "description": "a_description",
            "reference": "a_reference",
            "collection_cmd": "a_collection_cmd",
            "collection_cmd_type": "a_collection_cmd_type",
            "collect_only": false,
            "checks": [{{
                "id": "1",
                "description": "a_description",
                "type": "a_type",
                "cmd": "a_cmd",
                "expected": "a_expected",
                "verification_type": "a_verification_type",
                "cmd_output": "a_cmd_output",
                "result": true,
                "severity": "a_severity",
                "recommandation_on_failed": "a_recommandation_on_failed",
                "see_also": "a_see_also"
            }}]
        }}]
    }}
    """
    json_category = json.dumps(a_category, cls=ChecklistJsonEncoder)
    assert json.loads(json_category) == json.loads(expected_json)
