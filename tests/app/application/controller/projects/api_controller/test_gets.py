from app.infrastructure.db.entity.project import Project
from tests import client


class TestGet(object):
    def setup_method(self, method):  # noqa: ANN001, ANN201
        pass

    def test_get_num_0(self, mocker):  # noqa: ANN001, ANN201
        projects = []
        mocker.patch("app.infrastructure.db.repository.project_repository.find_all").return_value = projects

        response = client.get("/projects")
        assert response.status_code == 200

        response_body = response.json["projects"]
        assert len(response_body) == 0

    def test_get_num_1(self, mocker):  # noqa: ANN001, ANN201
        projects = [Project(id=1, name="name1")]
        mocker.patch("app.infrastructure.db.repository.project_repository.find_all").return_value = projects

        response = client.get("/projects")
        assert response.status_code == 200

        response_body = response.json["projects"]
        assert len(response_body) == 1

        assert response_body[0]["id"] == 1
        assert response_body[0]["name"] == "name1"

    def test_get_num_2(self, mocker):  # noqa: ANN001, ANN201
        projects = [Project(id=1, name="name1"), Project(id=2, name="name2")]
        mocker.patch("app.infrastructure.db.repository.project_repository.find_all").return_value = projects

        response = client.get("/projects")
        assert response.status_code == 200

        response_body = response.json["projects"]
        assert len(response_body) == 2

        assert response_body[0]["id"] == 1
        assert response_body[0]["name"] == "name1"

        assert response_body[1]["id"] == 2
        assert response_body[1]["name"] == "name2"
