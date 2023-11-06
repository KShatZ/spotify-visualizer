<h1 align="center">Spotify Visualizer</h1>

![App Preview Header Image](docs/readme-header.png)


<div align="center">
    <a href="#demo-the-mvp">Demo the MVP</a>
</div>


## Project Description

<br>
<br>

## Tech Used

### Front End:
The front-end is entirely built from flask rendered jinja templates that contain vanilla **HTML, CSS, and Javscript**. There are plans to port this all over to REACT.js once I get around to learning the framework.
<br>

### Back End:
The backend is all built with Pythons' **Flask** web framework, which has **Plottly Dash** attached to it as well. You can view the requirements.txt file for a list of all third-party tools being used.
<br>

### Database:
At the current moment, in order to allow for faster development and pivotting **MongoDB** is being used. There might be plans to utilize mongo more as a cache and transitition data over to a SQL based database in the future, once schemas and functionality is ironed out.
<br>

### Production Infrastructure:
In production, the application is containerized and run by a **Gunicorn** server which sits behind an **Nginx** proxy server. 

At the moment, the mongo database that is being used is hosted with Mongo Atlas.
<br>
<br>

## Run Project Locally

### Environment Variables:
Regardless, on whether you choose to run the app [Bare Metal](#bare-metal:) or with [Docker](#docker:) you will need to set the values of some environment variables in the *environment.sh* script file found in the docker directory which is located at the root of the project.

<br>
<p align="center">docker/environment.sh</p>

```
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
```

**FLASK_SECRET_KEY**

**FLASK_APP_MODE**

**MONGO_URI**

**SPOTIFY_CLIENT_ID**

**SPOTIFY_CLIENT_SECRET**

**SPOTIFY_REDIRECT_URI**

<br>

### Bare Metal:
<br>

### Docker:
<br>


<br>
<br>

## Demo the MVP

