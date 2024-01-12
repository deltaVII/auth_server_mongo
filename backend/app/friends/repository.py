from ..repository import PyMongoRepository
from bson.objectid import ObjectId


class FriendRepository(PyMongoRepository):
    '''
    этот класс нарушает принцип подстановки барбары лисков
    т.к. здесь работают только 2 метода
    '''
    collection_name = 'User'

    def add(
            self,
            user_to_id: str,
            user_from_id: str):

        return self.collection.update_one(
            {'_id': ObjectId(user_from_id)},
            {'$push': {'friends': ObjectId(user_to_id)}}
        ).modified_count

    def delete(
            self,
            user_to_id: str,
            user_from_id: str):

        return self.collection.update_one(
            {'_id': ObjectId(user_from_id)},
            {'$pull': {'friends': ObjectId(user_to_id)}}
        ).modified_count