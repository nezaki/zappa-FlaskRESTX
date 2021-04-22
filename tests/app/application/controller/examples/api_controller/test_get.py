from tests import client


class TestGet(object):
    def setup_method(self, method):  # noqa: ANN001, ANN201
        pass

    def test_get(self, mocker):  # noqa: ANN001, ANN201
        response = client.get("/examples")
        assert response.status_code == 200
        response_body = response.json
        assert len(response_body) == 5

        assert response_body.get("example_string") == "example"
        assert response_body.get("example_number") == 999
        assert response_body.get("example_datetime") == "2021-04-22T12:30:45+0900"
        assert response_body.get("example_boolean")
        assert response_body.get("example_enum") == "1"
