from flask import Blueprint

IndexBlueprint = Blueprint("index", __name__, template_folder="templates")
from spotify_visualizer.blueprints.index import routes
