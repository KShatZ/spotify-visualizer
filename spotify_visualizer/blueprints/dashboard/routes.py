from flask import render_template
from flask_login import login_required, current_user

from spotify_visualizer.blueprints.dashboard import DashboardBlueprint


@DashboardBlueprint.get("/dashboard")
@login_required
def render_dashboard_page():
    
    # TODO: Clean this up with
    template_vars = {
        "first_name": current_user.username,
        "display_name": current_user.spotify.get("display_name"),
        "followers": current_user.spotify["followers"].get("total"),
        "following": current_user.get_following_count(),
        "profile_url": current_user.spotify["external_urls"].get("spotify"),
        "profile_img": "https://scontent-mia3-1.xx.fbcdn.net/v/t1.18169-1/76895_1340453370099_2524662_n.jpg?stp=c28.28.349.349a_dst-jpg_s320x320&_nc_cat=103&ccb=1-7&_nc_sid=0c64ff&_nc_ohc=PVQFybhGYPMAX_yW09H&_nc_ht=scontent-mia3-1.xx&edm=AP4hL3IEAAAA&oh=00_AfCAztiuuvR4zVOldDgRBOVa12fqtZaoWclmUt_nbf5qMA&oe=65264CC4",
        "total_tracks": current_user.get_total_tracks(),
        "playlists": current_user.get_playlists()[0],
        "playlist_count": current_user.get_playlists()[1],
    }

    return render_template("dashboard/dashboard.html", t=template_vars)
