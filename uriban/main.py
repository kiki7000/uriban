from uriban.api import api
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

from uriban.router import auth

from uriban.database import Base, db


api.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.add_middleware(
    SessionMiddleware,
    secret_key=api.config.get("SECRET_KEY"),
)

api.include_router(auth.router)

db_password = api.config.get("DB_PASSWORD")
db.init_db(
    api,
    database_url=f"mysql://root:{db_password}@localhost:3306/uriban"
)


@api.on_event("startup")
def startup():
    api.logger.info("API Started")

    Base.metadata.create_all(bind=db.engine)
    db.engine.connect()
    api.logger.info("Database Connected")


@api.on_event("shutdown")
def shutdown():
    api.logger.info("API Shutdown")

    db.close_session()
    db.engine.dispose()
    api.logger.info("Database Disconnected")


@api.get("/")
def main():
    return {"Hello": "World"}
