from dataclasses import dataclass

from .errors import InvalidParameter


ACTIVITY_NAMES = (
    "top_rope",
    "lead",
    "bouldering",
)


@dataclass
class Activity:
    name: str

    def __post_init__(self):
        self.name = self.name.lower()
        self._validate_name()

    def _validate_name(self):
        if self.name not in ACTIVITY_NAMES:
            raise InvalidParameter(f"{self.name} is not a valid activity")

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name
