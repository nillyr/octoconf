# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoconf
# @since 1.0.0b

import json
import sys

import pytest

sys.path.append("../octoconf/")
from octoconf.components.json_encoders.checkresult import CheckResultJsonEncoder
from octoconf.models.check import CheckResult


def test_serialize_check_result():
    check_result = CheckResult(
        id="1",
        title="a_title",
        description="a_description",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        cmd_output="a_cmd_output",
        result=True,
        severity="a_severity",
        recommendation_on_failed="a_recommendation_on_failed",
        see_also="a_see_also",
    )

    expected_json = f"""
    {{
        "id": "1",
        "title": "a_title",
        "description": "a_description",
        "type": "a_type",
        "cmd": "a_cmd",
        "expected": "a_expected",
        "verification_type": "a_verification_type",
        "cmd_output": "a_cmd_output",
        "result": true,
        "severity": "a_severity",
        "recommendation_on_failed": "a_recommendation_on_failed",
        "see_also": "a_see_also"
    }}
    """

    json_check_result = json.dumps(check_result, cls=CheckResultJsonEncoder)
    assert json.loads(json_check_result) == json.loads(expected_json)
