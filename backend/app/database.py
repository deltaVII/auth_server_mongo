from abc import ABC, abstractmethod

from pymongo import MongoClient
from pymongo.database import Database


from config import DB_URL 



def get_database() -> Database:
    client = MongoClient(DB_URL)
    return client['main']


