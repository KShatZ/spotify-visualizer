from flask import Blueprint

SpotifyBlueprint = Blueprint("spotify", __name__)
from spotify_visualizer.blueprints.spotify import routes