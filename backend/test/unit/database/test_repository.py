from operator import attrgetter

from belay_me.model import Activity, Gym
from belay_me.database.repository import (
    ActivityRepository,
    GymRepository,
)


class TestGymRespository:
    def test_add(self, session):
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

    def test_get(self, session):
        session.execute("INSERT INTO gyms (name, address) VALUES ('Test Gym', '123 Testing Way')")
        session.execute(
            "INSERT INTO gym_activities (gym_name, activity_name) VALUES ('Test Gym', 'bouldering')"
        )
        session.execute(
            "INSERT INTO gym_activities (gym_name, activity_name) VALUES ('Test Gym', 'lead')"
        )

        repository = GymRepository(session)
        gym = repository.get("Test Gym")
        assert gym.name == "Test Gym"
        assert gym.address == "123 Testing Way"
        assert len(gym.activities) == 2

        # test gym-activity relationship
        assert sorted([a.name for a in gym.activities]) == ["bouldering", "lead"]

    def test_list(self, session):
        session.execute("INSERT INTO gyms (name, address) VALUES ('Test Gym 1', '123 Testing Way')")
        session.execute(
            """INSERT INTO gym_activities
            (gym_name, activity_name) VALUES ('Test Gym 1', 'bouldering')
            """
        )
        session.execute(
            "INSERT INTO gym_activities (gym_name, activity_name) VALUES ('Test Gym 1', 'lead')"
        )

        session.execute(
            """INSERT INTO gyms (name, address)
            VALUES ('Test Gym 2', '456 Testing Way')"""
        )
        session.execute(
            """INSERT INTO gym_activities
            (gym_name, activity_name)
            VALUES ('Test Gym 2', 'bouldering')"""
        )
        session.execute(
            "INSERT INTO gym_activities (gym_name, activity_name) VALUES ('Test Gym 2', 'top_rope')"
        )

        repository = GymRepository(session)
        gyms = sorted(repository.list(), key=attrgetter("name"))
        assert len(gyms) == 2

        g1, g2 = gyms[0], gyms[1]

        assert g1.name == "Test Gym 1"
        assert g1.address == "123 Testing Way"
        assert sorted([a.name for a in g1.activities]) == ["bouldering", "lead"]

        assert g2.name == "Test Gym 2"
        assert g2.address == "456 Testing Way"
        assert sorted([a.name for a in g2.activities]) == ["bouldering", "top_rope"]


class TestActivityRepository:
    def test_get(self, session):
        repository = ActivityRepository(session)
        a = repository.get("bouldering")
        assert a.name == "bouldering"

    def test_list(self, session):
        repository = ActivityRepository(session)
        activities = repository.list()
        assert len(activities) == 3
        assert sorted([a.name for a in activities]) == ["bouldering", "lead", "top_rope"]
