from belay_me.database import Session


def test_database_connection():
    with Session() as session:
        from pprint import pprint

        pprint(vars(session))
        res = session.execute("SELECT 1").first()
        assert res[0] == 1
