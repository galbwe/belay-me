import pytest

from belay_me import model


def test_model_import():
    assert model


def test_users_with_the_same_id_are_equal():
    u1 = model.create_user(
        id_=1,
        email="user1@gmail.com",
        birthday="2020-01-01",
        weight=120,
        skills={"top_rope": "5.10.a", "lead": "5.8", "bouldering": "V1"},
    )

    u2 = model.create_user(
        id_=1,
        email="user2@gmail.com",
        birthday="2020-01-02",
        weight=121,
        skills={"top_rope": "5.10.b", "lead": "5.9", "bouldering": "V2"},
    )

    assert u1 == u2


def test_users_with_different_ids_are_not_equal():
    u1 = model.create_user(
        id_=1,
        email="user1@gmail.com",
        birthday="2020-01-01",
        weight=120,
        skills={"top_rope": "5.10.a", "lead": "5.8", "bouldering": "V1"},
    )

    u2 = model.create_user(
        id_=2,
        email="user1@gmail.com",
        birthday="2020-01-01",
        weight=120,
        skills={"top_rope": "5.10.a", "lead": "5.8", "bouldering": "V1"},
    )

    assert u1 != u2


def test_user_repr_method():
    u = model.create_user(
        id_=1,
        email="user1@gmail.com",
        birthday="2020-01-01",
        weight=120,
        skills={"top_rope": "5.10.a", "lead": "5.8", "bouldering": "V1"},
    )

    assert repr(u).startswith("User(id_=1, email=")


@pytest.mark.parametrize(
    "email",
    [
        "sdfadsfasdfas",
        "sdfasdfasdf@",
        "aasdfad.com",
        "asdfsdaf@dsafsdf",
    ],
)
def test_validate_email(email):

    with pytest.raises(model.errors.InvalidParameter):
        model.create_user(
            id_=1,
            email=email,
            birthday="2020-01-01",
            weight=120,
            skills={"top_rope": "5.10.a", "lead": "5.8", "bouldering": "V1"},
        )
