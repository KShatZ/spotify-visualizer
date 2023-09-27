from flask import Flask
from flask_login import LoginManager


login_manager = LoginManager()


def init_app():
    """Initializes the Flask app

    :return: Flask App
    :rtype: Flask App Instance
    """

    app = Flask("__name__", template_folder="spotify_visualizer/templates", static_folder="spotify_visualizer/static")

    with app.app_context():

        login_manager.init_app(app)

        # ------ Config ------ #
        app.config["SECRET_KEY"] = "someSecretKey" # TODO: Proper

        # ------ Blueprints ------ #
        from .blueprints.index import IndexBlueprint
        app.register_blueprint(IndexBlueprint)
        from .blueprints.auth import AuthenticationBlueprint
        app.register_blueprint(AuthenticationBlueprint)
        from .blueprints.spotify import SpotifyBlueprint
        app.register_blueprint(SpotifyBlueprint)
        from .blueprints.dashboard import DashboardBlueprint
        app.register_blueprint(DashboardBlueprint)
        from .blueprints.playlist import PlaylistBlueprint
        app.register_blueprint(PlaylistBlueprint)
        
        # ------ Dash ------ #
        from .dash import create_dash_app
        app = create_dash_app(app)

        return app
