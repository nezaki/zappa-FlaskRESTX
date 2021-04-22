import os

from migrate.versioning.shell import main

if __name__ == "__main__":
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    database = os.environ.get("DB_DATABASE")
    user = os.environ.get("DB_USER_NAME")
    password = os.environ.get("DB_PASSWORD")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8"
    repository = "data_model/migration"

    main(debug="False", url=url, repository=repository)
