import os
from urllib.parse import urljoin

import pytest


@pytest.fixture(scope="session")
def environment():
    return {
        "API_URL": os.environ["API_URL"],
    }


@pytest.fixture(scope="session")
def base_url(environment):
    return environment["API_URL"]


@pytest.fixture(scope="session")
def url(base_url):
    def _url(path, schema="http"):
        if not base_url.startswith("http"):
            base_url = f"{schema}://{base_url}"
        return urljoin(base_url, path)

    return _url
