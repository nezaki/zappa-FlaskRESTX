from typing import Callable, Dict, NoReturn

from flask import request
from flask_restx import Namespace, Resource, marshal
from sqlalchemy.orm.session import Session

from app.application.controller.parse import parse_payload
from app.application.controller.response import BAD_REQUEST, NO_CONTENT, NOT_FOUND, OK
from app.application.model import project_schema, projects_schema, validation_errors_schema
from app.error import NotFound
from app.infrastructure.db.connection import db_connection
from app.infrastructure.db.entity.project import Project
from app.infrastructure.db.repository import project_repository
from app.infrastructure.db.util import payload_to_entity

namespace = Namespace(name="Projects", path="/projects", description="プロジェクト")

_project_model = project_schema.model()
_projects_model = projects_schema.model()
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

    @namespace.doc(description="プロジェクトの取得")
    @namespace.response(**OK, model=_projects_model)
    @db_connection()
    def get(self, db_session: Session):  # noqa: ANN201
        """プロジェクト取得API"""
        projects = project_repository.find_all(db_session)
        response = marshal({projects_schema.projects.title: [p.to_dict() for p in projects]}, fields=_projects_model)
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
        """プロジェクト更新API"""
        project = project_repository.find_by_id(db_session, project_id)
        payload_to_entity(Project, project, payload)
        response = marshal(project.to_dict(), fields=_project_model)
        return response, 200

    @namespace.doc(description="プロジェクトの取得")
    @namespace.response(**OK, model=_project_model)
    @namespace.response(**NOT_FOUND)
    @db_connection()
    def get(self, project_id: int, db_session: Session):  # noqa: ANN201
        """プロジェクト取得API"""
        project = project_repository.find_by_id(db_session, project_id)
        response = marshal(project.to_dict(), fields=_project_model)
        return response, 200

    @namespace.doc(description="プロジェクトの削除")
    @namespace.response(**NO_CONTENT)
    @namespace.response(**NOT_FOUND)
    @db_connection()
    def delete(self, project_id: int, db_session: Session):  # noqa: ANN201
        """プロジェクト削除API"""
        project_repository.delete(db_session, project_id)
        return None, 204
