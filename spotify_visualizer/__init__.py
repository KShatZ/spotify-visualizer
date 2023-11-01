from os import getenv

from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix


login_manager = LoginManager()


def init_app():
    """Initializes the Flask app

    :return: Flask App
    :rtype: Flask App Instance
    """
    
    PRODUCTION = getenv("FLASK_PRODUCTION", False)
    app = Flask("__name__", template_folder="spotify_visualizer/templates", static_folder="spotify_visualizer/static")

    with app.app_context():

        login_manager.init_app(app)

        # ------ Config ------ #
        app.config["SECRET_KEY"] = getenv("FLASK_SECRET_KEY", "someSecretKey")

        # ------ Middleware ------ #
        if PRODUCTION:
            # Behind Proxy - Sets how many headers to expect
            app.wsgi_app = ProxyFix(
                app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
            )


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
