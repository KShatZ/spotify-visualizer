from bson import ObjectId
from pymongo import MongoClient


mongo = MongoClient()
USERS_COLLECTION = mongo["spotify-visualizer"]["users"] # TODO: env vars


def create_user(user):
    """Inserts a user doc to the users collection.

    :param user: User document with account information
    :type user: Dict
    :return: _id of inserted user doc, or None if there was an issue
    :rtype: str
    """
    try:
        result = USERS_COLLECTION.insert_one(user)
        user_id = result.inserted_id
        
        if not user_id:
            return None
        
        return user_id
    
    except:
        # TODO Better error handling, maybe?
        return None


def get_user(user_id="", username=None):
    """Get user document based on _id or username. This function assumes that the
    user already exists, can ensure this by calling user_exists() beforehand.

    :param user_id: The _id of user, defaults to ""
    :type user_id: str, optional
    :param username: The username of user, defaults to None
    :type username: str, optional
    :return: The user document from mongo
    :rtype: dict
    """

    if username:
        return USERS_COLLECTION.find_one({"username": username}, {"hash": 0})
    
    return USERS_COLLECTION.find_one({"_id": ObjectId(user_id)}, {"hash": 0})


def user_exists(user_id="", username=None):
    """Helper function used to see if a user exists with the provided _id or username.

    :param user_id: The _id of user doc that is being checked for, defaults to ""
    :type user_id: str, optional
    :param username: The username of user doc that is being checked for, defaults to None
    :type username: str, optional
    :return: Whether the user exists
    :rtype: bool
    """
    if username:
        count = USERS_COLLECTION.count_documents({"username": username}, limit=1)
    else:
        count = USERS_COLLECTION.count_documents({"_id": ObjectId(user_id)}, limit=1)

    if count == 0:
        return False
    
    return True