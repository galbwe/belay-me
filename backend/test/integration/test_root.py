from typing import Dict

import requests


def test_root(environment: Dict[str, str]) -> None:
    url = f"http://{environment['API_URL']}"
    res = requests.get(url)
    assert res.status_code == 200
