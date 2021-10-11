from models.check import Check
from models.checkpoint import Checkpoint
from models.category import Category


def get_check():
    checkA = Check(
        id="1",
        description="a_description",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        recommandation_on_failed="a_recommandation_on_failed",
        see_also="a_see_also",
    )

    checkB = Check(
        id="1",
        description="a_description",
        type="a_type",
        cmd="a_cmd",
        expected="a_expected",
        verification_type="a_verification_type",
        recommandation_on_failed="a_recommandation_on_failed",
        see_also="a_see_also",
    )

    checks = []
    checks.append(checkA)
    checks.append(checkB)

    return checks


def checkpoint():
    return [
        Checkpoint(
            id="1",
            title="a_title",
            description="a_description",
            reference="a_reference",
            collection_cmd="a_collection_cmd",
            collection_cmd_type="a_collection_cmd_type",
            checks=get_check(),
        )
    ]


def test_category_model_init():
    a_checkpoint = checkpoint()
    a_category = Category(
        id=1,
        name="a_name",
        checkpoints=a_checkpoint,
    )

    assert a_category.id == 1
    assert a_category.name == "a_name"
    assert a_category.checkpoints == a_checkpoint
