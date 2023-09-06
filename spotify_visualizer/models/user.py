import os

from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
from flask_login import UserMixin
from pymongo import MongoClient



class User(UserMixin):

    def __init__(self, user_doc):
        self.id = user_doc["_id"]
        self.username = user_doc["username"]
        self.spotify = user_doc["spotify"] # Remove the token values eventually

