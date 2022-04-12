import pytest

from belay_me.database import Session
from belay_me.database.schema import start_mappers


@pytest.fixture
def session():
    start_mappers()

    with Session() as session:
        try:
            yield session
        finally:
            # clean up database
            session.execute("DELETE FROM gyms")
            session.commit()
