from bson import ObjectId
from pymongo import MongoClient
from werkzeug.security import check_password_hash

from spotify_visualizer.field_names import Mongo

mongo = MongoClient(host=Mongo.MONGO_URI)
USERS_COLLECTION = mongo["spotify-visualizer"]["users"]

def authenticate_password_hash(username, pwd):
    """Checks the provided pwd against the hash stored in mongo for the user
    with the provided username. This function assumes that the username exsits.

    :param username: a username of a user that exists in mongo
    :type username: str
    :param pwd: password for the account
    :type pwd: str
    :return: Whether or not the password is correct
    :rtype: bool
    """

    # Get hash from DB
    hash_doc = USERS_COLLECTION.find_one({"username": username}, {"_id": 0, "password": 1})

    # Compare hash with current pass
    correct_pwd = check_password_hash(hash_doc["password"], pwd)

    return correct_pwd
