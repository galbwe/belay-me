from sqlalchemy import MetaData, Table, Column, String, ForeignKey
from sqlalchemy.orm import registry, relationship

from ..model import Activity, Gym


metadata = MetaData()


activity_table = Table(
    "activities",
    metadata,
    Column("name", String(), primary_key=True),
)


gym_table = Table(
    "gyms",
    metadata,
    Column("name", String(), primary_key=True),
    Column("address", String()),
)


gym_activities_association_table = Table(
    "gym_activities",
    metadata,
    Column("gym_name", ForeignKey("gyms.name")),
    Column("activity_name", ForeignKey("activities.name")),
)


def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(Activity, activity_table)
    mapper_registry.map_imperatively(
        Gym,
        gym_table,
        properties={
            "activities": relationship(Activity, secondary=gym_activities_association_table)
        },
    )
