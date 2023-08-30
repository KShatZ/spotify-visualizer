from flask import Blueprint

SpotifyBlueprint = Blueprint("spotify", __name__)

from spotify_visualizer.spotify import routes