from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.orm import registry

from ..model import Gym


metadata = MetaData()


gym_table = Table(
    "gyms",
    metadata,
    Column("name", String(), primary_key=True),
    Column("address", String()),
)


# users = Table(
#     "users", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("email", String(), nullable=False),
#     Column("birthday", String(), nullable=False),
#     Column("weight", Integer, nullable=False),
# )


def start_mappers():
    mapper_registry = registry()

    mapper_registry.map_imperatively(Gym, gym_table)
