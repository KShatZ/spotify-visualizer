from flask import render_template
from flask_login import login_required, current_user

from spotify_visualizer.blueprints.dashboard import DashboardBlueprint


@DashboardBlueprint.get("/dashboard")
@login_required
def render_dashboard_page():
    
    # TODO: Clean this up with user and playlist object
    template_vars = {
        "first_name": current_user.username,
        "display_name": current_user.spotify.get("display_name"),
        "followers": current_user.spotify["followers"].get("total"),
        "following": current_user.get_following_count(),
        "profile_url": current_user.spotify["external_urls"].get("spotify"),
        "profile_img": current_user.get_profile_image(),
        "total_tracks": current_user.get_total_tracks(),
        "playlists": current_user.get_playlists()[0],
        "playlist_count": current_user.get_playlists()[1],
    }

    return render_template("dashboard/dashboard.html", t=template_vars)
