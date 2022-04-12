from dataclasses import dataclass
from operator import attrgetter
from typing import List

from .activity import Activity
from .errors import InvalidParameter


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
        return (hash(self.name) * hash(self.address)) % 10**19

    def _validate_activities(self):
        if not self.activities:
            raise InvalidParameter("activities cannot be empty")

        if not all(isinstance(a, Activity) for a in self.activities):
            raise InvalidParameter("activities must be instances of Activity dataclass")

        # check for duplicate activities
        if len(self.activities) != len(set(self.activities)):
            raise InvalidParameter("activities cannot be duplicated")

    def _sort_activities(self):
        self.activities = sorted(self.activities, key=attrgetter("name"))


def create_gym(name: str, address: str, activities: List[str]) -> Gym:
    return Gym(
        name=name,
        address=address,
        activities=[Activity(a) for a in activities],
    )
