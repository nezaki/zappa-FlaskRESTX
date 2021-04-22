import os
import logging

os.environ["STAGE"] = "local"
os.environ["LOG_LEVEL"] = logging.getLevelName(logging.DEBUG)

if __name__ == "__main__":
    from app.api import app
    app.run(debug=True, port=5000)
