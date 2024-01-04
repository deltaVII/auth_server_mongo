from datetime import datetime

from mongoengine import Document
from mongoengine import StringField, ListField
from mongoengine import DateTimeField, LazyReferenceField
from mongoengine import CASCADE, PULL


class User(Document):
    email = StringField(required=True, unique=True)
    username = StringField(max_length=50, required=True, unique=True)
    hashed_password = StringField(max_length=700, min_length=8, required=True)

    friends = ListField(LazyReferenceField('User', required=True))

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
    
