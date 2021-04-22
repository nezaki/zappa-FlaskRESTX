import os
from functools import wraps

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

_stage = os.environ.get("STAGE")

if _stage == "test":
    engine = None

elif _stage == "local":
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    database = os.environ.get("DB_DATABASE")
    username = os.environ.get("DB_USER_NAME")
    password = os.environ.get("DB_PASSWORD")
    url = URL.create(drivername="mysql+pymysql", host=host, port=port, database=database, username=username,
                     password=password)
    engine = create_engine(url, pool_size=2, max_overflow=2, pool_recycle=60)

else:
    engine = None


# from sqlalchemy import inspect
# inspector = inspect(engine)


def db_connection(): # noqa
    def decorator(func): # noqa
        @wraps(func) # noqa
        def wrapper(*args, **kwargs): # noqa
            session = None
            try:
                session = sessionmaker(bind=engine)()
                response = func(*args, **kwargs, db_session=session)
                session.commit()
                return response
            except Exception as e:
                if session:
                    session.rollback()
                raise e
            finally:
                if session:
                    session.close()
        return wrapper
    return decorator
