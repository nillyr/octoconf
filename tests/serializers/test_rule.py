# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import json
import sys

sys.path.append("../../octoconf/")
from octoconf.components.serializers.rule import RuleJsonEncoder
from octoconf.entities.rule import Rule


def test_serialize_rules():
    rule = Rule(
        id="a_rule_id",
        title="a_title",
        description="a_description",
        collection_cmd="a_collection_cmd",
        check="a_check",
        verification_type="a_verification_type",
        expected="a_expected",
        recommendation="a_recommendation",
        level="a_level",
        severity="a_severity",
        references=["a_first_reference"],
        output="a_output",
        compliant=False,
    )

    expected_json = f"""
    {{
        "id": "a_rule_id",
        "title": "a_title",
        "description": "a_description",
        "collection_cmd": "a_collection_cmd",
        "check": "a_check",
        "verification_type": "a_verification_type",
        "expected": "a_expected",
        "recommendation": "a_recommendation",
        "level": "a_level",
        "severity": "a_severity",
        "references": ["a_first_reference"],
        "output": "a_output",
        "compliant": false
    }}
    """

    json_rule = json.dumps(rule, cls=RuleJsonEncoder, ensure_ascii=False)
    assert json.loads(json_rule) == json.loads(expected_json)
