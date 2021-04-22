from datetime import datetime, timedelta, timezone

from flask_restx import Namespace, Resource, marshal

from app.application.model import example_schema

namespace = Namespace(
    name="Examples",
    path="/examples",
    description="サンプル",
)

_example_model = example_schema.model()


@namespace.route("")
class ExamplesApi(Resource):

    @namespace.doc(description="GETサンプル")
    @namespace.response(code=200, description="OK", model=_example_model)
    def get(self):  # noqa: ANN201
        """GETサンプルAPI"""
        datetime_ = datetime(year=2021, month=4, day=22, hour=12, minute=30, second=45, microsecond=0,
                             tzinfo=timezone(timedelta(hours=9)))
        response = marshal(
            {
                "example_string": "example",
                "example_number": 999,
                "example_datetime": datetime_,
                "example_boolean": True,
                "example_enum": "1",
            },
            fields=_example_model)
        return response, 200
