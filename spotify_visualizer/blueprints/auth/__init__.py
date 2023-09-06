from flask import Blueprint


AuthenticationBlueprint = Blueprint("authentication_blueprint", __name__, template_folder="templates")
from spotify_visualizer.blueprints.auth import routes
