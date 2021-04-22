from http import HTTPStatus
from typing import NoReturn

from tests import client


def test_not_found() -> NoReturn:
    response = client.get("/not-found-test")
    assert response.status_code == 404
    response_body = response.json
    assert response_body.get("message") == HTTPStatus.NOT_FOUND.description
