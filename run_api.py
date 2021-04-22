import logging
import os

os.environ["STAGE"] = "local"
os.environ["LOG_LEVEL"] = logging.getLevelName(logging.DEBUG)

os.environ["DB_USER_NAME"] = "root"
os.environ["DB_PASSWORD"] = "root"
os.environ["DB_HOST"] = "127.0.0.1"
os.environ["DB_PORT"] = "3306"
os.environ["DB_DATABASE"] = "zappa-flaskrestx"

if __name__ == "__main__":
    from app.api import app
    app.run(debug=True, port=5000)
