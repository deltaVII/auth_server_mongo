from datetime import datetime

from bson.objectid import ObjectId
from mongoengine import *
from mongoengine import queryset


class User(Document):
    email = StringField(required=True, unique=True)
    username = StringField(max_length=50, required=True, unique=True)
    hashed_password = StringField(max_length=700, min_length=8, required=True)
    roles = ListField(StringField(max_length=50, required=True))

    friends = ListField(LazyReferenceField('User', required=True, reverse_delete_rule=PULL))
    #friend_requests_to_user = ListField(LazyReferenceField(required=True)) # мне
    #friend_requests_from_user = ListField(LazyReferenceField(required=True)) # от меня

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(args, kwargs)


connect(host='mongodb://root:example@127.0.0.1:27017/main?authSource=admin')




User.friends
