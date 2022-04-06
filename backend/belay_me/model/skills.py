from dataclasses import dataclass
from typing import Optional


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
