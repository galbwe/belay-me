import os


def sqlalchemy_uri():
    # default = "postgresql://postgres:postgres@localhost:5432/belay_me"
    # return os.environ.get('SQLALCHEMY_URI', default)
    return os.environ["SQLALCHEMY_URI"]
