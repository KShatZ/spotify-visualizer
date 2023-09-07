from bson import ObjectId
from flask import current_app
from pymongo import MongoClient
import requests

from spotify_visualizer.blueprints.spotify.helpers.spotify import get_access_token, refresh_access_token


mongo = MongoClient()
USERS_COLLECTION =  mongo["spotify-visualizer"]["users"]

def get_user_info(user_id):
    """Queries users collection to get the spotify.user object
    which contains user info

    :param user_id: _id of the current user
    :type user_id: str
    :return: The user info that was queried
    :rtype: dict
    """
    
    spotify_doc = USERS_COLLECTION.find_one({"_id": ObjectId(user_id)}, {"spotify.user": 1, "_id": 0})
    
    user_info = spotify_doc["spotify"]["user"]
    return user_info


def get_users_total_tracks(app, user_id):
    """Sends a request to a spotify endpoint and returns the total
    number of tracks the current user has saved.

    :param user_id: _id of current user
    :type user_id: str
    :return: Total number of songs the user has saved
    :rtype: int
    """

    access = get_access_token(user_id)
    
    # TODO: Globals??
    endpoint = "https://api.spotify.com/v1/me/tracks"
    params = {"integer": 1}
    headers = {"Authorization": "Bearer " + access}

    try:
        r = requests.get(endpoint, params=params, headers=headers)
        
        # Invalid Access Token - Refresh Needed           
        if r.status_code == 401:

            refreshed = refresh_access_token(user_id)

            if not refreshed:
                # TODO: Issue with refreshing
                return None
            
            app.logger.info(f"Refreshed Access for user: {user_id}")
            return get_users_total_tracks(app, user_id)

        data = r.json()
        total_tracks = data["total"]

        return total_tracks
    
    except Exception as e:
        # TODO: Better error handling
        return None
