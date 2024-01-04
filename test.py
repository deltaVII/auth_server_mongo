from datetime import datetime

from bson.objectid import ObjectId
from mongoengine import *
from mongoengine import queryset


class User(Document):
    email = StringField(required=True, unique=True)
    username = StringField(max_length=50, required=True, unique=True)
    hashed_password = StringField(max_length=700, min_length=8, required=True)
    roles = ListField(StringField(max_length=50, required=True))

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(args, kwargs)


class UserSession(Document):
    token = StringField(max_length=1000, required=True, unique=True)
    user_id = LazyReferenceField(User, reverse_delete_rule=CASCADE, required=True)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(args, kwargs)
connect(host='mongodb://root:example@127.0.0.1:27017/main?authSource=admin')



q=UserSession.objects(token='123').update(token='456')

print(q)