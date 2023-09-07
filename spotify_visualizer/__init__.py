from flask import Flask
from flask_login import LoginManager


login_manager = LoginManager()


def init_app():
    """Initializes the Flask app

    :return: Flask App
    :rtype: Flask App Instance
    """

    app = Flask("__name__", static_folder="spotify_visualizer/static")

    login_manager.init_app(app)

    with app.app_context():

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
        
        # ------ Dash ------ #
        from .dash import create_dash_app
        app = create_dash_app(app)

        return app
