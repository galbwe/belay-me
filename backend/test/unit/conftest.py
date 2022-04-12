import pytest

from belay_me.database import Session
from belay_me.database.schema import start_mappers

from sqlalchemy.orm import clear_mappers


@pytest.fixture
def session():
    start_mappers()

    with Session() as session:
        try:
            session.execute(
                """
                INSERT into activities (name)
                VALUES ('bouldering'), ('lead'), ('top_rope');
            """
            )
            yield session
        finally:
            clear_mappers()
            # clean up database
            session.execute("DELETE FROM gym_activities")
            session.execute("DELETE FROM activities")
            session.execute("DELETE FROM gyms")
            session.commit()
