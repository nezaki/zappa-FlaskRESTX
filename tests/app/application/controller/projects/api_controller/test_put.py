from app.infrastructure.db.entity.project import Project
from tests import client


class TestPut(object):
    def setup_method(self, method):  # noqa: ANN001, ANN201
        pass

    def test_put(self, mocker):  # noqa: ANN001, ANN201
        id_ = 2
        payload = {
            "id": id_,
            "name": "テスト",
        }
        project = Project(**payload)
        mocker.patch("app.infrastructure.db.repository.project_repository.find_by_id").return_value = project

        del payload["id"]
        response = client.put(f"/projects/{id_}", json=payload)
        assert response.status_code == 200

        response_body = response.json
        assert len(response_body) == 2
        assert response_body["id"] == id_
        assert response_body["name"] == payload["name"]
