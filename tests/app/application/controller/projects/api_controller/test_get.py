from app.infrastructure.db.entity.project import Project
from tests import client


class TestGet(object):
    def setup_method(self, method):  # noqa: ANN001, ANN201
        pass

    def test_get_200(self, mocker):  # noqa: ANN001, ANN201
        id_ = 1
        project = Project(id=id_, name="name1")
        mocker.patch("app.infrastructure.db.repository.project_repository.find_by_id").return_value = project

        response = client.get(f"/projects/{id_}")
        assert response.status_code == 200

        response_body = response.json
        assert response_body["id"] == id_
        assert response_body["name"] == "name1"

    def test_get_404(self, mocker):  # noqa: ANN001, ANN201
        id_ = 2
        projects = None
        mocker.patch("app.infrastructure.db.repository.project_repository.find_by_id").return_value = projects

        response = client.get(f"/projects/{id_}")
        assert response.status_code == 404
