# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

sys.path.append("../../octoconf/")
from octoconf.entities.rule import Rule


def test_rule_result_model_init():
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
        compliant=True,
    )

    assert rule.id == "a_rule_id"
    assert rule.title == "a_title"
    assert rule.description == "a_description"
    assert rule.collection_cmd == "a_collection_cmd"
    assert rule.check == "a_check"
    assert rule.verification_type == "a_verification_type"
    assert rule.expected == "a_expected"
    assert rule.recommendation == "a_recommendation"
    assert rule.level == "a_level"
    assert rule.severity == "a_severity"
    assert rule.references == ["a_first_reference"]
    assert rule.output == "a_output"
    assert rule.compliant == True
