from datetime import datetime

from bson.objectid import ObjectId

from ..repository import DatedPyMongoRepository, PyMongoRepository


class UserRepository(DatedPyMongoRepository):
    '''
    username: str
    email: str
    hashed_password: str
    
    sessions: [{
        token: str
        created_at: datetime
        update_at: datetime
    }]
    friends: [ObjectId(User)]

    created_at: datetime
    update_at: datetime
    '''
    collection_name = 'User'

    def add_one(self, data: dict) -> str:
        data['friends'] = []
        return super().add_one(data)
    

class UserSessionRepository(PyMongoRepository):
    '''
    этот класс нарушает принцип подстановки барбары лисков
    т.к. здесь работают только 3 метода

    token: str
    created_at: datetime
    update_at: datetime
    '''
    collection_name = 'User'

    def insert_one(self, user_id: str, token: str) -> int:
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)}, 
            {'$push': {'sessions': {
                'token': token,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }}}
        )
        return result.modified_count

    def update_one(self, old_token: str, new_token: str) -> int:
        result = self.collection.update_one(
            {'sessions.token': old_token}, 
            {'$set': {
                'sessions.$.token': new_token,
                'sessions.$.updated_at': datetime.utcnow()
            }}
        )
        return result.modified_count
    
    def delete_one(self, token: str) -> int:
        result = self.collection.update_one(
            {'sessions.token': token}, 
            {'$pull': {
                'sessions': {'token': token}
            }}
        )
        return result.modified_count