from models.check import Check


def test_check_model_init():
    check = Check(
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

    assert check.id == "1"
    assert check.description == "a_description"
    assert check.type == "a_type"
    assert check.cmd == "a_cmd"
    assert check.expected == "a_expected"
    assert check.verification_type == "a_verification_type"
    assert check.severity == "a_severity"
    assert check.recommandation_on_failed == "a_recommandation_on_failed"
    assert check.see_also == "a_see_also"
