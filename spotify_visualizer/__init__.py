from flask import Flask


def init_app():
    """Initializes the Flask app

    :return: Flask App
    :rtype: Flask App Instance
    """

    app = Flask("__name__")

    with app.app_context():

        # App Configuration & Imports
        from .spotify import SpotifyBlueprint

        app.register_blueprint(SpotifyBlueprint)

        # Importing Dash application
        from .dash import create_dash_app
        app = create_dash_app(app)


        return app