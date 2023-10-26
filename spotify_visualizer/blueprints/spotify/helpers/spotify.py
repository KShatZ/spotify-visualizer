from pymongo import MongoClient
import requests
# from dotenv import load_dotenv
# load_dotenv()

from spotify_visualizer.field_names import Mongo

mongo = MongoClient(host=Mongo.MONGO_URI)
USERS_COLLECTION = mongo["spotify-visualizer"]["users"]


def get_spotify_user_info(access_token):
    """Sends a request to the user profile spotify endpoint
    and returns a dict with the user info data.

    :param access_token: access_token for the current user
    :type access_token: str
    :return: User info data
    :rtype: dict
    """

    # TODO: Global??
    endpoint = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer " + access_token}

    try:
        # Make a request to the user endpoint
        r = requests.get(endpoint, headers=headers)

        if r.status_code == 401:
            print("Access Token Expired")
            # This should usually never happen, unless I call this function elsewhere.
            # refresh_function()

        data = r.json()

        # Clean data that is not needed
        data.pop("uri")
        data.pop("explicit_content")

        return data
    except:
        print("handle some error")
        return None