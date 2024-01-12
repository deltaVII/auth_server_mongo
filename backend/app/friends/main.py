from bson.objectid import ObjectId

from ..auth.main import get_user
from ..auth.repository import UserRepository

def is_users_friends(
        firstuser_id: str,
        seconduser_id: str,
        user_repository: UserRepository) -> bool:
    
    firstuser = user_repository.get_by_id(firstuser_id)
    seconduser = user_repository.get_by_id(seconduser_id)


    if (firstuser['id'] in [i.id for i in seconduser['friends']] and 
        seconduser['id'] in [i.id for i in firstuser['friends']]):

        return True
    
    return False






