from tests import client


class TestDelete(object):
    def setup_method(self, method):  # noqa: ANN001, ANN201
        pass

    def test_delete(self, mocker):  # noqa: ANN001, ANN201
        mocker.patch("app.infrastructure.db.repository.project_repository.find_by_id")
        mocker.patch("app.infrastructure.db.repository.project_repository.delete")
        response = client.delete("/projects/1")
        assert response.status_code == 204
