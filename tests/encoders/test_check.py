# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json
import sys

sys.path.append("../octoreconf/")
from octoreconf.components.json_encoders import CheckJsonEncoder
from octoreconf.models.check import Check


def test_serialize_checks():
    a_check = Check(
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

    expected_json = f"""
    {{
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
    }}
    """

    json_check = json.dumps(a_check, cls=CheckJsonEncoder)
    assert json.loads(json_check) == json.loads(expected_json)
