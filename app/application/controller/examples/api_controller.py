from flask_restx import Namespace, Resource, marshal

from app.application.model import example_schema
from app.util.datetime import get_jst_now

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
        response = marshal(
            {
                "example_string": "example",
                "example_number": 999,
                "example_datetime": get_jst_now(),
                "example_boolean": True,
                "example_enum": "1",
            },
            fields=_example_model)
        return response, 200
