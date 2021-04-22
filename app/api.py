import json
import logging
import os
from typing import Any, Tuple

from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api
from http import HTTPStatus
import traceback


_STAGE = os.environ.get("STAGE", "local")
_LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARN")


class LocalConfig:
    DEBUG = True
    ENV = os.environ.get("STAGE", "local")
    SWAGGER_UI_DOC_EXPANSION = "list"  # 'none', 'list' or 'full'
    SWAGGER_SUPPORTED_SUBMIT_METHODS = [
        "get", "put", "post", "delete", "options", "head", "patch", "trace"]
    RESTX_MASK_SWAGGER = False


CONFIG_NAME_MAPPER = {
    "local": LocalConfig,
}


def _add_model(api_: Api, schema: Any) -> None:
    model = schema.model()
    api_.models[model.name] = model


def create_app() -> Tuple[Flask, Api]:
    config = CONFIG_NAME_MAPPER[_STAGE]
    app = Flask("zappa FlaskRESTX")
    app.config.from_object(config)
    app.logger.setLevel(_LOG_LEVEL)
    CORS(app=app, origins="*", allow_headers="*")

    api = Api(
        app=app,
        version="0.0.1",
        title="zappa FlaskRESTX",
        description="zappa FlaskRESTX Description",
        doc="/" if _STAGE in ["local"] else False,
        validate=False,
        ordered=False,
        prefix="",
    )
    namespaces = []
    schemas = []

    api.namespaces.clear()
    [api.add_namespace(namespace) for namespace in namespaces]
    [_add_model(api, schema) for schema in schemas]

    @app.before_request
    def before_request() -> None:
        if logging.getLevelName(_LOG_LEVEL) <= logging.DEBUG:
            request_body = json.dumps(request.json, indent=2, ensure_ascii=False) \
                if request.json else None
            app.logger.debug(
                "\n===========\nrequest\n==========="
                f"\nurl: {request.method} {request.url}"
                f"\n{request.headers}"
                f"body: {request_body}")

    @app.after_request
    def after_request(response): # noqa
        if logging.getLevelName(_LOG_LEVEL) <= logging.DEBUG:
            response_body = json.dumps(response.json, indent=2, ensure_ascii=False) if response.json else None
            app.logger.debug(
                "\n\n===========\nresponse\n==========="
                f"\nstatus: {response.status}"
                f"\n{response.headers}"
                f"\nbody: {response_body}")
        return response

    @api.errorhandler(404)
    def not_found_error(ex):
        return {"message": HTTPStatus.NOT_FOUND.description}, HTTPStatus.NOT_FOUND.value

    return app, api


app, api = create_app()


@api.errorhandler(Exception)
def error_handler(ex):  # noqa
    app.logger.error(traceback.format_exc())
    return {"message": HTTPStatus.INTERNAL_SERVER_ERROR.description}, HTTPStatus.INTERNAL_SERVER_ERROR.value
