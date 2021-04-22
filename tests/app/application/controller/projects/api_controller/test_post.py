from tests import client


class TestPost(object):
    def setup_method(self, method):  # noqa: ANN001, ANN201
        pass

    def test_post(self, mocker):  # noqa: ANN001, ANN201
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
