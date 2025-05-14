from os import getenv

from bson import ObjectId
from pymongo import MongoClient
import requests
# from dotenv import load_dotenv
# load_dotenv()

from spotify_visualizer.blueprints.spotify.helpers.spotify import get_spotify_user_info
from spotify_visualizer.field_names import Mongo


mongo = MongoClient(Mongo.MONGO_URI)
USERS_COLLECTION = mongo["spotify-visualizer"]["users"]


def populate_user_spotify_object(username, spotify_user_data):
    """Populates the 'spotify' key in the doc belonging to the provided username.

    :param username: username of the account doc to modify
    :type username: str
    :param spotify_user_data: The response received when swapping auth code for access token
    :type spotify_user_data: dict
    :return: Whether or not the spotify field was updated
    :rtype: bool
    """

    spotify_doc = {
        "access": spotify_user_data["access_token"],
        "refresh": spotify_user_data["refresh_token"],
        "scope":  spotify_user_data["scope"],
        "user": get_spotify_user_info(spotify_user_data["access_token"])
    }

    result = USERS_COLLECTION.update_one({"username": username}, {"$set": {"spotify": spotify_doc}})

    if result.modified_count == 0:
        return False  
    
    return True


def get_access_token(user_id):
    """Returns the spotify access_token belonging to the user
    with user_id provided

    :param user_id: The _id of the user
    :type user_id: str
    :return: Access token belonging to user
    :rtype: str
    """

    spotify_doc = USERS_COLLECTION.find_one({"_id": ObjectId(user_id)}, {"spotify.access": 1, "_id": 0})

    access_token = spotify_doc["spotify"]["access"]

    return access_token


def refresh_access_token(user_id):
    """Refreshes the spotify API access token, for the user provided.

    :param user_id: The _id of the user to refresh token for
    :type user_id: str
    :return: Refreshed Access Token or None
    :rtype: str
    """ 

    spotify_doc = USERS_COLLECTION.find_one({"_id": ObjectId(user_id)}, {"spotify": 1, "_id": 0})

    if not spotify_doc: 
        # TODO: Handle this, either user does not exist or spotify object not set up (need to auth)
        # But this should basically never happen
        print("No spotify doc for user refresh")
        return None
    
    # TODO: Globals???
    endpoint = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "refresh_token",
        "refresh_token": spotify_doc["spotify"]["refresh"],
        "client_id": getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": getenv("SPOTIFY_CLIENT_SECRET"),
    }

    r = requests.post(endpoint, headers=headers, params=body, timeout=60)
    response_data = r.json()

    access_token = response_data["access_token"]
    
    update_result = USERS_COLLECTION.update_one({"_id": ObjectId(user_id)}, {"$set": {"spotify.access": access_token}})
    if update_result.modified_count == 0:
        # Document wasnt modified for some reason -- handle TODO
        return None

    return access_token
