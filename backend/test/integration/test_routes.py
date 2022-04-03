from urllib.parse import urljoin

import pytest
import requests


@pytest.fixture
def check_status_code(environment):
    def _check_status_code(method: str, route: str, expected_status_code: int, **kwargs):

        http_methods = {
            "get": requests.get,
            "post": requests.post,
            "put": requests.put,
            "delete": requests.delete,
            "patch": requests.patch,
        }

        method_name = method.lower()
        http_method = http_methods[method_name]
        url = urljoin(f"http://{environment['API_URL']}", route)

        res = http_method(url, **kwargs)
        assert res.status_code == expected_status_code

    return _check_status_code


def routes():
    return [
        ("GET", "/", 200),
        ("GET", "/healthcheck", 200),
        *user_routes(),
    ]


def user_routes():
    routes = [
        ("GET", "/api/v1/users", 200),
    ]
    return routes


@pytest.mark.parametrize("method, route, expected_status_code", routes())
def test_routes(check_status_code, method, route, expected_status_code):
    check_status_code(method, route, expected_status_code)
