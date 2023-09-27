from flask import Blueprint


PlaylistBlueprint = Blueprint("playlist_blueprint", __name__, template_folder="templates")
from spotify_visualizer.blueprints.playlist import routes