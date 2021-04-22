from typing import Callable, Dict, NoReturn

from flask import request
from flask_restx import Namespace, Resource, marshal
from sqlalchemy.orm.session import Session

from app.application.controller.parse import parse_payload
from app.application.controller.response import BAD_REQUEST, NOT_FOUND, OK
from app.application.model import project_schema, validation_errors_schema
from app.error import NotFound
from app.infrastructure.db.connection import db_connection
from app.infrastructure.db.entity.project import Project
from app.infrastructure.db.repository import project_repository
from app.infrastructure.db.util import payload_to_entity

namespace = Namespace(name="Projects", path="/projects", description="プロジェクト")

_project_model = project_schema.model()
_validation_errors_model = validation_errors_schema.model()


@namespace.route("")
class ProjectsApi(Resource):

    @namespace.doc(description="プロジェクトの登録")
    @namespace.expect(_project_model)
    @namespace.response(**OK, model=_project_model)
    @namespace.response(**BAD_REQUEST)
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


@namespace.route("/<int:project_id>")
class ProjectApi(Resource):

    @db_connection()
    def validate_payload(self, func: Callable, db_session: Session) -> NoReturn:
        project_id = request.view_args.get("project_id")
        if project_repository.find_by_id(db_session, project_id) is None:
            raise NotFound

    @namespace.doc(description="プロジェクトの更新")
    @namespace.expect(_project_model)
    @namespace.response(**OK, model=_project_model)
    @namespace.response(**BAD_REQUEST)
    @namespace.response(**NOT_FOUND)
    @parse_payload(model=_project_model)
    @db_connection()
    def put(self, project_id: int, payload: Dict, db_session: Session):  # noqa: ANN201
        """プロジェクト登録API"""
        project = project_repository.find_by_id(db_session, project_id)
        payload_to_entity(Project, project, payload)
        response = marshal(project.to_dict(), fields=_project_model)
        return response, 200
