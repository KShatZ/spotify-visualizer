from os import getenv

from spotify_visualizer import init_app


DEBUG = getenv("DEBUG", None)

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=DEBUG)
