from typing import Generator

from pymongo import MongoClient
from pymongo.database import Database

from ps_api.config import CFG

mongo = MongoClient(
    host=CFG.MONGO_HOST,
    port=CFG.MONGO_PORT,
    username=CFG.MONGO_USERNAME,
    password=CFG.MONGO_PASSWORD,
)


def get_db() -> Generator[Database, None, None]:
    # TODO: begin transaction
    yield mongo[CFG.MONGO_DB]
    # TODO: end transaction
