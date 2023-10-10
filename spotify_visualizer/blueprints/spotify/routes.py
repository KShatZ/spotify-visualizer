import os

from dotenv import load_dotenv
from flask import request, redirect
from flask_login import current_user
import requests
from urllib.parse import urlencode

from spotify_visualizer.blueprints.spotify import SpotifyBlueprint
from spotify_visualizer.blueprints.spotify.helpers.user import populate_user_spotify_object

load_dotenv()


@SpotifyBlueprint.get("/spotify/auth")
def spotify_auth():

    # NOTE: Might want to offload this like stfy-field_name??
    auth_code_params = {
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"), 
        "response_type": "code",
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "scope":"user-library-read user-read-private playlist-read-private user-follow-read",
        "show_dialog": True
    }

    endpoint = "https://accounts.spotify.com/authorize?" + urlencode(auth_code_params)
    return redirect(endpoint)


@SpotifyBlueprint.get("/spotify/auth/validate")
def validate_auth_code():

    auth_code = request.args.get("code", None)

    if not auth_code:
        # TODO
        # No code sent in redirect -- some sort of error or user did not accept Spotify OAuth
        # NOTE: request.args.get("error") will contain the error msg from Spotify

        print("No auth code present")
        return redirect("/")
    
    # ------ Swap Auth Code For Access Token ------ # 
    endpoint = "https://accounts.spotify.com/api/token"
    access_token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    access_token_params = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"), 
    }

    r = requests.post(endpoint, headers=access_token_headers, params=access_token_params)

    spotify_auth = populate_user_spotify_object(current_user.username, r.json())

    if not spotify_auth:
        # TODO: Take care of when user does not get updated
        return redirect("/login")

    return redirect("/")