#!/bin/bash

# ------ Flask Configuration ------ #
export FLASK_SECRET_KEY="someSecretKey"
export FLASK_APP_MODE=" PROD || DEV "

# ------ Mongo ------ #
export MONGO_URI=mongodb://mongo:27017

# SPOTIFY oAuth
export SPOTIFY_CLIENT_ID="Your Spotify App Client ID"
export SPOTIFY_CLIENT_SECRET="Your Spotify App Client Secret"
export SPOTIFY_REDIRECT_URI="URL To Redirect After Spotify oAUTH"