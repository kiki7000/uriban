from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = ("Base", "Database", "db")


class Database:
    def __init__(self):
        self.api = None

        self._engine = None
        self._session = None

    def init_db(self, api: FastAPI, database_url: str):
        self.api = api

        self._engine = create_engine(database_url)
        self._session = sessionmaker(autoflush=False, autocommit=False, bind=self._engine)

    def get_db(self):
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    def close_session(self):
        self._session.close_all()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = Database()
Base = declarative_base()
