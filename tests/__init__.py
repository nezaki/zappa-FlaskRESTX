from app.api import app


def run():  # noqa: ANN201
    app.testing = True
    return app.test_client()


client = run()
