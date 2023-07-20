# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

import pytest

sys.path.append("../../octoconf/")
from octoconf.entities.rule import Rule
from octoconf.entities.category import Category


@pytest.fixture
def my_rules():
    ruleA = Rule(
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
    )

    ruleB = Rule(
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
    )

    rules = []
    rules.append(ruleA)
    rules.append(ruleB)

    return rules


def test_category_model_init(my_rules):
    cat = Category(
        category="a_category",
        name="a_name",
        description="a_description",
        rules=my_rules,
    )

    assert cat.category == "a_category"
    assert cat.name == "a_name"
    assert cat.description == "a_description"
    assert cat.rules == my_rules
