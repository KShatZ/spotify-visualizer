from flask import request, render_template, redirect, current_app
from flask_login import login_required, current_user

from spotify_visualizer.blueprints.dashboard import DashboardBlueprint
from spotify_visualizer.blueprints.dashboard.helpers.user import get_user_info, get_users_total_tracks


@DashboardBlueprint.get("/dashboard")
@login_required
def render_dashboard_page():
    
    user_id = current_user.id
    user_info = get_user_info(user_id)

    template_vars = {
        "first_name": current_user.username,
        "display_name": user_info["display_name"],
        "followers": user_info["followers"]["total"],
        "profile_url": user_info["external_urls"]["spotify"],
        "total_tracks": get_users_total_tracks(current_app, user_id)
    }

    return render_template("dashboard.html", t=template_vars)
