import requests


def test_root(environment):
    url = f"http://{environment['API_URL']}"
    res = requests.get(url)
    assert res.status_code == 200
