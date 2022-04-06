import pytest
from belay_me import model


def test_gym_activities_cannot_be_empty():
    with pytest.raises(model.errors.InvalidParameter):
        model.Gym(
            name="Belay Me",
            address="123 Fake St",
            activities=[],
        )


def test_gym_activities_cannot_be_duplicated():
    with pytest.raises(model.errors.InvalidParameter):
        model.Gym(
            name="Belay Me",
            address="123 Fake St",
            activities=[
                model.Activity.TOP_ROPE,
                model.Activity.TOP_ROPE,
            ],
        )


def test_gym_activities_must_be_in_enum():
    with pytest.raises(model.errors.InvalidParameter):
        model.Gym(
            name="Belay Me",
            address="123 Fake St",
            activities=[
                "sdfsdfsdfs",
            ],
        )


def test_gym_activity_order_doesnt_change_equality():
    gym1 = model.Gym(
        name="Belay Me",
        address="123 Fake St",
        activities=[
            model.Activity.TOP_ROPE,
            model.Activity.LEAD,
        ],
    )
    gym2 = model.Gym(
        name="Belay Me",
        address="123 Fake St",
        activities=[
            model.Activity.LEAD,
            model.Activity.TOP_ROPE,
        ],
    )
    assert gym1 == gym2


def test_gym_factory_method():
    gym = model.create_gym(
        "Belay Me",
        "123 Fake St",
        ["top_rope", "lead", "bouldering"],
    )
    assert gym == model.Gym(
        name="Belay Me",
        address="123 Fake St",
        activities=[
            model.Activity.TOP_ROPE,
            model.Activity.LEAD,
            model.Activity.BOULDERING,
        ],
    )
