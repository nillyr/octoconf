# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import json
import sys

import pytest

sys.path.append("../../octoconf/")
from octoconf.components.serializers.baseline import BaselineJsonEncoder
from octoconf.entities.baseline import Baseline
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
            compliant=False
        )
    ]


@pytest.fixture
def my_categories(my_rules):
    return [
        Category(
            category="a_category",
            name="a_name",
            description="a_description",
            rules=my_rules,
        )
    ]


def test_serialize_baseline(my_categories):
    baseline = Baseline(
        title="a_title",
        categories=my_categories,
    )

    expected_json = f"""
    {{
        "title": "a_title",
        "categories": [{{
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
        }}]
    }}
    """

    json_baseline = json.dumps(baseline, cls=BaselineJsonEncoder, ensure_ascii=False)
    assert json.loads(json_baseline) == json.loads(expected_json)
