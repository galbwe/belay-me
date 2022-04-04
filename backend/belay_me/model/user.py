from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict

from .errors import InvalidParameter

from email_validator import validate_email, EmailNotValidError


@dataclass
class YosemiteDecimalRating:
    level: int  # 0 - 16
    sublevel: Optional[str]  # abcd


@dataclass
class VScaleRating:
    level: int  # 0 - 7


Rating = YosemiteDecimalRating | VScaleRating | None


@dataclass
class Skills:
    top_rope: Rating
    lead: Rating
    bouldering: Rating


class User:
    def __init__(
        self,
        id_: int,
        email: str,
        birthday: datetime,
        weight: int,  # weight lbs,
        skills: Skills,
    ):
        self._validate_email(email)

        self.id_ = id_
        self.email = email
        self.birthday = birthday
        self.weight = weight
        self.skills = skills

    def __repr__(self):
        params = [
            f"id_={self.id_!r}",
            f"email={self.email!r}",
            f"birthday={self.birthday.strftime('%Y-%m-%d')!r}",
            f"weight={self.weight!r}",
            f"skills={self.skills!r}",
        ]
        return "User(" + ", ".join(params) + ")"

    def __eq__(self, other):
        return self.id_ == other.id_

    def _validate_email(self, email: str):
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise InvalidParameter(f"email: {email}") from e


def create_rating(r: Optional[str]) -> Rating:
    if r is None:
        return None
    if r.lower().startswith("v"):
        return _create_v_scale_rating(r)
    return _create_yosemite_decimal_rating(r)


def _create_v_scale_rating(r: str) -> Rating:
    level = int(r[1:])
    return VScaleRating(level)


def _create_yosemite_decimal_rating(r: str) -> Rating:
    levels = r.split(".")
    level = levels[1]
    sublevel = levels[2] if len(levels) > 2 else None
    return YosemiteDecimalRating(int(level), sublevel)


def create_skills(
    top_rope: Optional[str], lead: Optional[str], bouldering: Optional[str]
) -> Skills:
    return Skills(
        top_rope=create_rating(top_rope),
        lead=create_rating(lead),
        bouldering=create_rating(bouldering),
    )


def create_user(
    id_: int,
    email: str,
    birthday: str,
    weight: int,  # weight lbs,
    skills: Dict[str, str],
):
    return User(
        id_, email, datetime.strptime(birthday, "%Y-%m-%d"), weight, create_skills(**skills)
    )
