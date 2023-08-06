# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import sys

import pytest

sys.path.append("../../octoconf/")
from octoconf.entities.rule import Rule
from octoconf.entities.category import Category
from octoconf.entities.baseline import Baseline


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


def test_baseline_model_init(my_categories):
    baseline = Baseline(
        title="a_title",
        categories=my_categories,
    )

    assert baseline.title == "a_title"
    assert baseline.categories == my_categories
