from bson.objectid import ObjectId

from ..auth.main import get_user


def is_users_friends(
        firstuser_id: str,
        seconduser_id: str) -> bool:
    
    firstuser = get_user(firstuser_id)
    seconduser = get_user(seconduser_id)


    if (firstuser.id in [i.id for i in seconduser.friends] and 
        seconduser.id in [i.id for i in firstuser.friends]):

        return True
    
    return False






