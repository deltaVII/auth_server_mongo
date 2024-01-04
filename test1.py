import pymongo
from bson.objectid import ObjectId

# устанавливаем соединение с MongoDB
# MongoDB должна быть запущена на компьютере, 27017 - стандартный порт
db_client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")  # MongoClient('localhost', 27017)

# подключаемся к БД pyloungedb, если её нет, то будет создана
current_db = db_client["main"]  # dictionary style
# current_db = db_client.pyloungedb - attribute style

# получаем колекцию из нашей БД, если её нет, то будет создана
# Коллекция - это группа документов, которая хранится в БД MongoDB (эквалент таблицы в ркляционных базах)
collection_user = current_db["users"]  # current_db.youtubers
'''collection_user.update_one(
    {'_id': ObjectId('658ec429ae12681439439367')},
    {
        '$push': {'sessions': '123'}
    })'''

'''collection_user.update_one(
    {'_id': ObjectId('658ec429ae12681439439367'), 'sessions': '123'},
    {'$set': {'sessions.$': '456'}}
)'''

user_session = collection_user.update_one(
        {'sessions': token},
        {'$pull': {'sessions': token}}
    )


    