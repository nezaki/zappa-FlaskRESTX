from tests import client


class TestPost(object):
    def setup_method(self, method):  # noqa: ANN001, ANN201
        pass

    def test_post_200(self, mocker):  # noqa: ANN001, ANN201
        payload = {
            "name": "テスト"
        }
        mocker.patch("app.infrastructure.db.repository.project_repository.create")
        mocker.patch("sqlalchemy.orm.session.Session.flush")

        response = client.post("/projects", json=payload)
        assert response.status_code == 200

        response_body = response.json
        assert len(response_body) == 2
        # assert response_body["id"] ==
        assert response_body["name"] == payload["name"]

    def test_post_400(self, mocker):  # noqa: ANN001, ANN201
        payload = {
            "name": 1
        }
        response = client.post("/projects", json=payload)
        assert response.status_code == 400

        response_errors = response.json["errors"]
        assert len(response_errors) == 1
        assert response_errors[0]["field"] == "name"
        assert len(response_errors[0]["code"]) == 1
