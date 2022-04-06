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


def test_changing_activities_does_not_change_gym_identity():
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
        ],
    )
    assert gym1 == gym2


def test_gyms_with_different_name_are_unequal():
    gym1 = model.Gym(
        name="Belay Me",
        address="123 Fake St",
        activities=[
            model.Activity.TOP_ROPE,
            model.Activity.LEAD,
        ],
    )
    gym2 = model.Gym(
        name="Belay Me Too",
        address="123 Fake St",
        activities=[
            model.Activity.TOP_ROPE,
            model.Activity.LEAD,
        ],
    )
    assert gym1 != gym2


def test_gyms_with_different_addresses_are_unequal():
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
        address="456 Fake St",
        activities=[
            model.Activity.TOP_ROPE,
            model.Activity.LEAD,
        ],
    )
    assert gym1 != gym2


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


def test_gym_repr_method():
    gym = model.create_gym(
        "Belay Me",
        "123 Fake St",
        ["top_rope", "lead", "bouldering"],
    )

    def expected_activity(a: str):
        return f"<Activity.{a.upper()}: {a!r}>"

    top_rope = expected_activity("top_rope")
    lead = expected_activity("lead")
    bouldering = expected_activity("bouldering")
    assert repr(gym) == (
        f"Gym(name='Belay Me', address='123 Fake St', "
        f"activities=[{bouldering}, {lead}, {top_rope}])"
    )


def test_gyms_are_hashable():
    gym1 = model.create_gym(
        "Belay Me",
        "123 Fake St",
        ["top_rope", "lead", "bouldering"],
    )
    gym2 = model.create_gym(
        "Belay Me",
        "123 Fake St",
        ["top_rope", "lead"],
    )
    gym3 = model.create_gym(
        "Belay Me Too!",
        "456 Fake St",
        ["top_rope", "lead", "bouldering"],
    )
    assert hash(gym1) == hash(gym2) and gym1 == gym2
    assert hash(gym1) != hash(gym3) and gym1 != gym3
