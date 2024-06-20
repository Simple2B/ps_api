import os
import tomllib
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PYPROJECT_TOML = os.path.join(BASE_DIR, "pyproject.toml")
PROJECT_ENV = os.path.join(BASE_DIR, "project.env")


def get_poetry_value(name: str) -> str:
    with open(PYPROJECT_TOML, "rb") as f:
        return tomllib.load(f)["tool"]["poetry"][name]


class Config(BaseSettings):
    """Configuration."""

    APP_NAME: str = get_poetry_value("name")
    VERSION: str = get_poetry_value("version")

    SECRET_KEY: str = "api_super_secret_key"
    BASE_DIR: str = BASE_DIR

    STATIC_DIR: str = os.path.join(BASE_DIR, "ps_api", "static")
    APP_PORT: int = 8080

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=(PROJECT_ENV, ".env"),
    )
    TESTING: bool = False


CFG = Config()
