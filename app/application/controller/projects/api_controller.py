from typing import Dict

from flask_restx import Namespace, Resource, marshal
from sqlalchemy.orm.session import Session

from app.application.controller.parse import parse_payload
from app.application.model import project_schema, validation_errors_schema
from app.infrastructure.db.connection import db_connection
from app.infrastructure.db.entity.project import Project
from app.infrastructure.db.repository import project_repository

namespace = Namespace(
    name="Projects",
    path="/projects",
    description="プロジェクト",
)

_project_model = project_schema.model()
_validation_errors_model = validation_errors_schema.model()


@namespace.route("")
class ProjectApi(Resource):

    @namespace.doc(description="プロジェクトの登録")
    @namespace.expect(_project_model)
    @namespace.response(code=200, description="OK", model=_project_model)
    @namespace.response(code=400, description="Bad Request", model=_validation_errors_model)
    @parse_payload(model=_project_model)
    @db_connection()
    def post(self, payload: Dict, db_session: Session):  # noqa: ANN201
        """プロジェクト登録API"""
        project = Project(**payload)
        project.created_by = 1  # TODO
        project_repository.create(db_session, project)
        db_session.flush()
        response = marshal(project.to_dict(), fields=_project_model)
        return response, 200
