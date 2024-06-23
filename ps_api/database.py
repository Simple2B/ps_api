from typing import Generator

from pymongo import MongoClient
from pymongo.database import Database

from ps_api.config import CFG

mongo = MongoClient(CFG.MONGO_URI)


def get_db() -> Generator[Database, None, None]:
    yield mongo[CFG.MONGO_DB]
