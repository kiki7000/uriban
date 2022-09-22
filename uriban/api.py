from subprocess import check_output
from logging import getLogger, Formatter, StreamHandler, FileHandler, getLevelName
from termcolor import colored

from fastapi import FastAPI

from starlette.config import Config
from authlib.integrations.starlette_client import OAuth


__all__ = ("API", "api")


class API(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = self
        self.config = Config(".env")
        self.logger = None

        self.oauth = OAuth(self.config)
        self.oauth.register(
            name="google",
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "email"},
        )

        self.set_handler()

    def set_handler(self):
        self.logger = getLogger("uriban")
        self.logger.setLevel(
            getLevelName(self.config.get("LOG_LEVEL", default="INFO").upper())
        )

        console_handler = StreamHandler()
        console_handler.setFormatter(
            Formatter(
                f"[{colored('%(asctime)s', 'cyan')}] (%(filename)s:{colored('%(lineno)d', 'yellow')}) %(name)s:{colored('%(levelname)s', 'grey')} - %(message)s"
            )
        )

        file_handler = FileHandler("uriban.log")
        file_handler.setFormatter(
            Formatter(
                f"[%(asctime)s] (%(filename)s:%(lineno)d) %(name)s:%(levelname)s - %(message)s"
            )
        )

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)


version = check_output(["git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()

api = API(
    title="Uriban",
    version=version,
    terms_of_service="",
    description="""
    """,

    contact={
        "name": "Woohyun Jung",
        "url": "https://github.com/kiki7000",
        "email": "devkiki7000@gmail.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },

    docs_url="/swagger-docs",
    redoc_url="/docs",
)
