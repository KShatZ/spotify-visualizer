from flask import Blueprint

DashboardBlueprint = Blueprint("dashboard", __name__, template_folder="templates")
from spotify_visualizer.blueprints.dashboard import routes