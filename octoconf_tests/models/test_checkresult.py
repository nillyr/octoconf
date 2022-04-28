# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

sys.path.append("../octoconf/")
from octoconf.models.check import CheckResult


def test_checkresult_model_init():
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
        level="a_level",
        recommendation_on_failed="a_recommendation_on_failed",
        see_also="a_see_also",
    )

    assert check_result.id == "1"
    assert check_result.title == "a_title"
    assert check_result.description == "a_description"
    assert check_result.type == "a_type"
    assert check_result.cmd == "a_cmd"
    assert check_result.expected == "a_expected"
    assert check_result.verification_type == "a_verification_type"
    assert check_result.cmd_output == "a_cmd_output"
    assert check_result.result == True
    assert check_result.severity == "a_severity"
    assert check_result.level == "a_level"
    assert check_result.recommendation_on_failed == "a_recommendation_on_failed"
    assert check_result.see_also == "a_see_also"
