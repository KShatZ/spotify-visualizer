from flask import request, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user

from pymongo import MongoClient

from werkzeug.security import generate_password_hash


from spotify_visualizer.blueprints.auth import AuthenticationBlueprint
from spotify_visualizer.blueprints.auth.helpers.user import get_user, user_exists, create_user
from spotify_visualizer.blueprints.auth.helpers.password import authenticate_password_hash
from spotify_visualizer.models.user import User
from spotify_visualizer import login_manager


@login_manager.user_loader
def load_user(user_id):
    """Required function for flask_login. Retrieves user document from MongoDB
    by querying on provided user_id, and returns a new instance of the User class.

    :param user_id: The _id of a user document
    :type user_id: str
    :return: User object created with the user doc
    :rtype: object
    """
    
    user_doc = get_user(user_id)

    if user_doc is None:
        return None
    
    return User(user_doc)

@login_manager.unauthorized_handler
def unauthorized():
    """This handler is called when someone tries to access a path where
    being logged in is required. Therefore, redirects user to the login
    screen.
    """
    
    return redirect("/login")


@AuthenticationBlueprint.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

    
@AuthenticationBlueprint.get("/register")
def render_register_page():

    return render_template("register.html")


@AuthenticationBlueprint.post("/register")
def post_register():

    user = request.json

    # TODO: Sanitize values, before sending to DB

    if (user_exists(username=user["username"])):
        return "someStatusCode: Username exists" #TODO

    user["spotify"] = None
    user["password"] = generate_password_hash(user["password"])

    user_id = create_user(user)

    if not user_id:
        return "someStatusCode: There was an issue creating an account at this time. Please Try Again."
    
    print(f"Created New User: ObjectId({user_id})")
    return {
        "msg": "User created."
    }, 201


@AuthenticationBlueprint.get("/login")
def render_login_page():

    if current_user.is_authenticated:
        redirect("/")
        
    return render_template("login.html")


@AuthenticationBlueprint.post("/login")
def login():

    # TODO: Better handling - i.e. in the case where username or password do not exist
    username = request.json.get("username") 
    password = request.json.get("password") 

    # TODO: Need to sanitize the data before passing into database

    user = get_user(username=username)

    if not user:
        # TODO: Log invalid login attempt
        return "someStatusCode Username and/or password does not match our records"
    
    if not authenticate_password_hash(username, password):
        # TODO: Log invalid login attempt
        return "someStatusCode Username and/or password does not match our records"
    
    try:
        logged_in = login_user(User(user))

        if not logged_in:
            return "someStatusCode couldn't log in for some reason"

        # Spotify OAuth Required
        if user["spotify"] == None:
            print(f"User {user['username']}: Did not have spotify object, redirecting to spotify auth...")
            return {
                "msg": f"The account with username {user['username']} has not setup spotify."
            }, 401
        
        return {
            "msg": "Logged In"
        }, 200

    except:
        #TODO: Better error handling
        return "someStatusCode Issues logging in"
