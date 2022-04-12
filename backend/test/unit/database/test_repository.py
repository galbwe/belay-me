from belay_me.model import Activity, Gym
from belay_me.database.repository import GymRepository


def test_add_gym(session):
    repository = GymRepository(session)
    gym = Gym(
        "Test Gym",
        "123 Testing Way",
        [
            session.query(Activity).filter(Activity.name == "bouldering").first(),
        ],
    )
    repository.add(gym)
    session.commit()

    # query the gyms table to make sure a gym was added
    res = session.execute("SELECT name, address FROM gyms where name = 'Test Gym'").all()
    assert len(res) == 1
    gym = res[0]
    assert gym[0] == "Test Gym"
    assert gym[1] == "123 Testing Way"

    # query the gym_activities table to make sure the gym has the activity
    res_2 = session.execute(
        "SELECT activity_name from gym_activities where gym_name = 'Test Gym'"
    ).all()
    assert len(res_2) == 1
    assert res_2[0][0] == "bouldering"
