# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

from models.check import CheckResult


def test_checkresult_model_init():
    check_result = CheckResult(
        id="1",
        description="a_description",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        cmd_output="a_cmd_output",
        result=True,
        severity="a_severity",
        recommandation_on_failed="a_recommandation_on_failed",
        see_also="a_see_also",
    )

    assert check_result.id == "1"
    assert check_result.description == "a_description"
    assert check_result.type == "a_type"
    assert check_result.cmd == "a_cmd"
    assert check_result.expected == "a_expected"
    assert check_result.verification_type == "a_verification_type"
    assert check_result.cmd_output == "a_cmd_output"
    assert check_result.result == True
    assert check_result.severity == "a_severity"
    assert check_result.recommandation_on_failed == "a_recommandation_on_failed"
    assert check_result.see_also == "a_see_also"
