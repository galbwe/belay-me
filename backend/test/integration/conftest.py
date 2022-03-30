from typing import Dict, Callable

import os
from urllib.parse import urljoin

import pytest


@pytest.fixture(scope="session")
def environment() -> Dict[str, str]:
    return {
        "API_URL": os.environ["API_URL"],
    }


@pytest.fixture(scope="session")
def base_url(environment: Dict[str, str]) -> str:
    return environment["API_URL"]


@pytest.fixture(scope="session")
def url(base_url: str) -> Callable[..., str]:
    def _url(path: str, schema: str = "http") -> str:
        nonlocal base_url
        if not base_url.startswith("http"):
            base_url = f"{schema}://{base_url}"
        return urljoin(base_url, path)

    return _url
