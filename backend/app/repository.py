from datetime import datetime

from pymongo.collection import Collection
from pymongo.database import Database
from pydantic import BaseModel
from bson.objectid import ObjectId


class PyMongoRepository:
    collection: Collection = None
    collection_name: str = ''

    def __init__(self, database: Database) -> None:
        self.collection = database[self.collection_name]

    def _serialization_input(self, data: dict) -> dict:
        '''
        заменяет все айди: str на айди: ObjectId
        '''
        for key, value in zip(data.keys(), data.values()):
            if key.endswith('id'):
                data[key] = ObjectId(data[key])
            if isinstance(value, dict):
                self._serialization_input(value)
            if isinstance(value, list):
                for i in value:
                    if isinstance(i, dict):
                        self._serialization_input(i)

    def _serialization_output(self, data: dict) -> dict:
        '''
        заменяет все айди: ObjectId на айди: str
        '''
        for key, value in zip(data.keys(), data.values()):
            if key.endswith('id'):
                data[key] = data[key].__str__()
            if isinstance(value, dict):
                self._serialization_output(value)
            if isinstance(value, list):
                for i in value:
                    if isinstance(i, dict):
                        self._serialization_output(i)


    def add_one(self, data: dict) -> str:
        self._serialization_input(data)
        return self.collection.insert_one(data).inserted_id
    
    def get_by_id(self, object_id: str) -> dict:
        result = self.collection.find_one({'_id': ObjectId(object_id)})
        self._serialization_output(result)
        return result
    
    def find(self, filters: dict) -> list[dict]:
        self._serialization_input(filters)
        results = self.collection.find(filters)
        mass = []
        for result in results:
            result['id']=result['_id'].__str__() 
            self._serialization_output(result)
            mass.append(result)
        return mass
    
    def find_one(self, filters: dict) -> list[dict]:
        self._serialization_input(filters)
        result = self.collection.find_one(filters)
        if result is not None:
            result['id'] = result['_id'].__str__()
            self._serialization_output(result)
            return result
    
    def update_one(self, filters: dict, data: dict) -> int:
        return self.collection.update_one(filters, data).modified_count
    
    def delete_one(self, filters: dict) -> int:
        return self.collection.delete_one(filters).deleted_count


class DatedPyMongoRepository(PyMongoRepository):
    def add_one(self, data: dict) -> str:
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()

        return super().add_one(data)
    
    def update_one(self, filters: dict, data: dict) -> int:
        data['updated_at'] = datetime.utcnow()
        
        return super().update_one(filters, data)