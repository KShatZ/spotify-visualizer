from spotify_visualizer.blueprints.index import IndexBlueprint

from flask import render_template, redirect
from flask_login import current_user



@IndexBlueprint.get("/")
def get_homepage():

    if current_user.is_authenticated:
        return redirect("/dashboard")

    return render_template("login.html")
