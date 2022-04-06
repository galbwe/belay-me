from belay_me import model


def test_skills_are_value_objects():
    s1 = model.create_skills(
        top_rope="5.10.a",
        lead="5.9",
        bouldering="v1",
    )
    s2 = model.create_skills(
        top_rope="5.10.a",
        lead="5.9",
        bouldering="v1",
    )
    s3 = model.create_skills(
        top_rope="5.10.b",
        lead="5.9",
        bouldering="v1",
    )
    s4 = model.create_skills(
        top_rope="5.10.a",
        lead="5.8",
        bouldering="v1",
    )
    s5 = model.create_skills(
        top_rope="5.10.a",
        lead="5.9",
        bouldering="v2",
    )
    assert s1 == s2
    assert s1 != s3
    assert s1 != s4
    assert s1 != s5
