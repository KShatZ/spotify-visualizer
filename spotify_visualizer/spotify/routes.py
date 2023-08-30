from spotify_visualizer.spotify import SpotifyBlueprint

@SpotifyBlueprint.get("/")
def hello_world1():
    return "Hello World"
