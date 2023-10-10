from flask import request, render_template
from flask_login import current_user, login_required

from spotify_visualizer.blueprints.playlist import PlaylistBlueprint
from spotify_visualizer.models.playlist import Playlist


@PlaylistBlueprint.get("/playlist/<playlist_id>")
@login_required
def render_playlist_page(playlist_id):
    
    if playlist_id == "liked-songs":
        playlist = Playlist(source="mongo")
        template = "liked-songs.html"
    else:
        playlist = Playlist(playlist_id, source="mongo")
        template = "playlist.html"

    # TODO: Need better method, to not refresh on empty playlists each time -- even though rare
    if playlist.total_tracks == 0:
        playlist.update_playlist_tracks()
    
    update = False
    if request.args.get("update"): # NOTE: Maybe might need specific check later on...
        update = True

    return render_template(template, playlist=playlist, update=update)


@PlaylistBlueprint.post("/playlist/update/<playlist_id>")
@login_required
def update_playlist(playlist_id):

    try:
        if playlist_id == "liked-songs":
            playlist = Playlist(source="spotify")
        else:
            playlist = Playlist(playlist_id, source="spotify")
    except:
        return {
            "msg": "Issue updating playlist"
        }, 500
    
    return {
        "msg": f"Playlist {playlist_id} updated",
        "playlist": {
            "id": playlist.id
        },
    }, 200
    