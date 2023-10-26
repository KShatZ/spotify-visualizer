from os import getenv

class Mongo:
    MONGO_URI = getenv("MONGO_URI", "localhost")

class Status:
    OK = 200
    CREATED = 201
    UNAUTHORIZED = 401
    SERVER_ERROR = 500


class CAMELOT:

    MAJOR = {
        "E": "12B",
        "B": "1B",
        "Fs": "2B",
        "Df": "3B",
        "Af": "4B",
        "Ef": "5B",
        "Bf": "6B",
        "F": "7B",
        "C": "8B",
        "G": "9B",
        "D": "10B",
        "A": "11B",
    }
    
    MINOR = {
        "Df": "12A",
        "Af": "1A",
        "Ef": "2A",
        "Bf": "3A",
        "F": "4A",
        "C": "5A",
        "G": "6A",
        "D": "7A",
        "A": "8A",
        "E": "9A",
        "B": "10A",
        "Fs": "11A",
    }
    
    PITCH_CLASS = {
        "0": "C",
        "1": "Df",
        "2": "D",
        "3": "Ef",
        "4": "E",
        "5": "F",
        "6": "Fs",
        "7": "G",
        "8": "Af",
        "9": "A",
        "10": "Bf",
        "11": "B",
    }
