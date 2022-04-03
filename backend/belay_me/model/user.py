from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class YosemiteDecimalRating:
    level: int  # 0 - 16
    sublevel: Optional[str]  # abcd


@dataclass
class VScaleRating:
    level: int  # 0 - 7


@dataclass
class Skills:
    top_rope: YosemiteDecimalRating
    lead: YosemiteDecimalRating
    bouldering: VScaleRating


class User:
    def __init__(
        self,
        id: int,
        email: str,
        birthday: datetime,
        weight: int,  # weight lbs,
        skills: Skills,
    ):
        self.id = id
        self.email = email
        self.birthday = birthday
        self.weight = weight
        self.skills = skills
