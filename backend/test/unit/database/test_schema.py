import belay_me.model as model


def test_gym_model_creates_records_in_gym_table(session):
    gym = model.Gym(
        name="Test Gym",
        address="123 Testing Way",
        activities=[
            session.query(model.Activity).filter(model.Activity.name == "bouldering").first(),
            session.query(model.Activity).filter(model.Activity.name == "lead").first(),
            session.query(model.Activity).filter(model.Activity.name == "top_rope").first(),
        ],
    )
    session.add(gym)
    session.commit()

    del gym

    gym_2 = session.query(model.Gym).filter(model.Gym.address == "123 Testing Way").first()
    activities = [a.name for a in gym_2.activities]
    assert "bouldering" in activities
    assert "lead" in activities
    assert "top_rope" in activities
