from datetime import datetime
from typing import Dict

from .errors import InvalidParameter
from .skills import Skills, create_skills

from email_validator import validate_email, EmailNotValidError


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
