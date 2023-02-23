# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import json
import sys

import pytest

sys.path.append("../../octoconf/")
from octoconf.components.serializers.category import CategoryJsonEncoder
from octoconf.entities.category import Category
from octoconf.entities.rule import Rule


@pytest.fixture
def my_rules():
    return [
        Rule(
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
    ]


def test_serialize_category(my_rules):
    cat = Category(
        category="a_category",
        name="a_name",
        description="a_description",
        rules=my_rules,
    )

    expected_json = f"""
    {{
        "category": "a_category",
        "name": "a_name",
        "description": "a_description",
        "rules": [{{
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
        }}]
    }}
    """

    json_category = json.dumps(cat, cls=CategoryJsonEncoder, ensure_ascii=False)
    assert json.loads(json_category) == json.loads(expected_json)
