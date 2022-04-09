from belay_me.database.repository import GymRepository
from belay_me.model import create_gym


def test_add_gym(session):
    repository = GymRepository(session)
    gym = create_gym("Test Gym", "123 Testing Way", ["bouldering"])
    repository.add(gym)
    session.commit()

    # query the gyms table to make sure a gym was added
    res = session.execute("SELECT name, address FROM gyms where name = 'Test Gym'").all()
    assert len(res) == 1
    gym = res[0]
    assert gym[0] == "Test Gym"
    assert gym[1] == "123 Testing Way"
