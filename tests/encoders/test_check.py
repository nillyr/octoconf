# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import json

from components.json_encoders import CheckJsonEncoder
from models.check import Check


def test_serialize_checks():
    a_check = Check(
        id="1",
        description="a_description",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        severity="a_severity",
        recommandation_on_failed="a_recommandation_on_failed",
        see_also="a_see_also",
    )

    expected_json = f"""
    {{
        "id": "1",
        "description": "a_description",
        "type": "a_type",
        "cmd": "a_cmd",
        "expected": "a_expected",
        "verification_type": "a_verification_type",
        "cmd_output": "",
        "result": "",
        "severity": "a_severity",
        "recommandation_on_failed": "a_recommandation_on_failed",
        "see_also": "a_see_also"
    }}
    """

    json_check = json.dumps(a_check, cls=CheckJsonEncoder)
    assert json.loads(json_check) == json.loads(expected_json)
