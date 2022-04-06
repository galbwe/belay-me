from dataclasses import dataclass
from enum import Enum, unique
from operator import attrgetter
from typing import List

from .errors import InvalidParameter


@unique
class Activity(Enum):
    TOP_ROPE = "top_rope"
    LEAD = "lead"
    BOULDERING = "bouldering"


@dataclass
class Gym:
    name: str
    address: str
    activities: List[Activity]

    def __post_init__(self):
        self._validate_activities()
        self._sort_activities()

    def __eq__(self, other):
        return self.name == other.name and self.address == other.address

    def __hash__(self):
        return (hash(self.name) * hash(self.address)) % 19

    def _validate_activities(self):
        if not self.activities:
            raise InvalidParameter("activities cannot be empty")

        if not all(isinstance(a, Activity) for a in self.activities):
            raise InvalidParameter("activities must be Activity enum values")

        # check for duplicate activities
        if len(self.activities) != len(set(self.activities)):
            raise InvalidParameter("activities cannot be duplicated")

    def _sort_activities(self):
        self.activities = sorted(self.activities, key=attrgetter("value"))


def create_gym(name: str, address: str, activities: List[str]) -> Gym:
    return Gym(
        name=name,
        address=address,
        activities=[Activity(a) for a in activities],
    )
