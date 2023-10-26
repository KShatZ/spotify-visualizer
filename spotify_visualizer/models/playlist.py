import datetime

from flask_login import current_user
from pymongo import MongoClient

from spotify_visualizer.blueprints.spotify.helpers.user import get_access_token, refresh_access_token
from spotify_visualizer.helpers.spotify_api import SpotifyRequest
from spotify_visualizer.models.track import Track
from spotify_visualizer.field_names import Mongo


class Playlist():

    def __init__(self, id=None, source="mongo", debug=False):
        """Constructor that creates a playlist either based on the
        information stored in it's mongo collection (default) or
        from a fresh spotify pull.

        :param user_id: The _id of the current user
        :type user_id: str
        :param playlist_id: The spotify id of the playlist to create. 
        If none, then 'Liked Songs', defaults to None
        :type playlist_id: str, optional
        :param source: The source from where to create the playlist 
        
            "mongo": Will create the playlist object from the data
            stored in the playlist's mongo collection.

            "spotify": Will create the playlist object from a fresh
            request to the spotify api. This will also update the
            mongo collection.

            defaults to "mongo"
        :type source: str, optional
        """

        self.id = id
        self.user_id = current_user.id
        self.debug = debug

        mongo = MongoClient(Mongo.MONGO_URI)

        # Liked Songs
        if not self.id:
            self.PLAYLIST_COLLECTION = mongo[str(self.user_id)]["liked_songs"]
            self.meta = self.PLAYLIST_COLLECTION.find_one({"_id": "meta"})
            
        # Playlist
        if self.id:            
            self.PLAYLIST_COLLECTION = mongo[str(self.user_id)][str(self.id)]
            self.meta = self.PLAYLIST_COLLECTION.find_one({"_id": "meta"})
            
        if self.meta:
            self.name = self.meta.get("name")
        
        self.track_docs = list(self.PLAYLIST_COLLECTION.find({"_id": {"$ne": "meta"}})) 
        self.total_tracks = len(self.track_docs)
        
        if self.total_tracks == 0:
            self.track_docs = []

        self.tracks = [Track(track, debug=True) for track in self.track_docs]
        if source == "spotify":
            self.update_playlist_tracks()


    def update_playlist_tracks(self, type="update"):
        """Entry point into updating the playlist.

        :param type: Whether to use batch mode or not, defaults to "update"
        :type type: str, optional
        """

        if self.total_tracks == 0:
            type="batch"

        playlist = None
        if self.id: # Not liked songs
            playlist = self.__playlist_meta()

        if self.debug:
            print(f"Playlist Update Type: {type}")

        self.__modify_playlist(playlist=playlist, type=type)
        
        self.tracks = [Track(track, debug=True) for track in self.track_docs]

    
    def update_needed(self, recent_track_count):
        """Checks whether or not the playlist needs
        to be updated.

        :param recent_track_count: The most recent count of
        tracks in the playlist
        :type recent_track_count: int
        :return: Whether or not the playlist needs to be updated
        :rtype: bool
        """

        # Playlist not in mongo - need to update to add
        if self.total_tracks == 0 and recent_track_count != 0:
            return True
        
        if self.total_tracks != recent_track_count:
            return True
        
        return False
    

    def get_total_duration_string(self):
        """Calculates the total duration of the playlist
        and returns a string to be used on the front-end for
        playlist meta information. 
        
        If the playlist is less than 1 hour long, the string will
        only include minutes and seconds.

        :return: Total duration of the playlist as a string
        formated "{} hours {} minutes {} seconds"
        :rtype: str
        """

        # NOTE: Fieldnames??
        HOURS = "hours"
        MINUTES = "minutes"
        SECONDS = "seconds"
        
        total_ms = 0

        for track in self.tracks:
            total_ms += track.duration_ms

        # Hour(s), Minute(s), Second(s)
        h = total_ms // 3600000
        m = (total_ms % 3600000) // 60000
        s = (total_ms % 60000) // 1000

        # Singluar
        if h == 1:
            HOURS = HOURS.rstrip("s")
        if m == 1:
            MINUTES = MINUTES.rstrip("s")
        if s == 1:
            SECONDS = SECONDS.rstrip("s")

        if h == 0:
            return f"{m} {MINUTES} {s} {SECONDS}"
        
        return f"{h} {HOURS} {m} {MINUTES} {s} {SECONDS}" 


    def delete_playlist():
        pass


    def __get_audio_features(self, tracks):
        """Sends a request to Spotify API for each provided 
        track to get their basic audio features. The response
        is added to the track doc under the key 'audio features'.

        This function utilizes the batch endpoint and sends multiple
        track id's in one request. If the audio features are needed for
        multiple tracks, this function is recommended over the single
        track version.

        :param tracks: A list of track docs. Can not contain more than 100
        as that is the max for the spotify endpoint.
        :type tracks: list of dics
        :return: The list of track docs, which have been modified
        with a new key 'audio_features'
        :rtype: list of dics
        """
        
        total_tracks = len(tracks)

        if total_tracks > 100: # TODO: Better Handling
            print("Get Audio Features: Can only get audio features for 100 tracks max...")
            return tracks 

        track_ids = ""
        for track in tracks:
            id = track["track"].get("id", None)

            if id:
                id = str(id) + ","
                track_ids += id

        params = {"ids": track_ids}

        r = SpotifyRequest("get", "https://api.spotify.com/v1/audio-features", params=params, debug=True)
        data = r.send().json()

        audio_features = data.get("audio_features")
        
        # TODO: Better error handling
        if total_tracks != len(audio_features):
            print("Track Audio Feature: Issue getting all tracks")
            return tracks
        
        for index, track_features in enumerate(audio_features):

            track_id = track_features.get("id")

            track = tracks[index]

            if track_id == track["track"].get("id"):
                track["audio_features"] = track_features
            else:
                # TODO: Better Handling in case order is not the same ever
                print("Wrong ID")

        return tracks


    def __liked_songs_meta(self, total_tracks):
        """For the 'Liked Songs' playlist return
        it's meta information.

        :param total_tracks: The total number of liked songs
        :type total_tracks: int
        :return: 'Liked Songs' meta information
        :rtype: dict
        """

        return {
            "_id": "meta",
            "name": "Liked Songs",
            "total_tracks": total_tracks,
            "user_id": self.user_id,
            "updated_at": datetime.datetime.now()
        }


    def __playlist_meta(self):
        """For regular playlist's sends a request to 
        the spotify playlist endpoint in order to retrieve
        meta information on the playlist as well as the first
        round of tracks.

        :return: The playlist meta info and the first round of tracks
        :rtype: Dict
        """

        endpoint = f"https://api.spotify.com/v1/playlists/{self.id}"
        params = {
            "fields": "external_urls,followers,id,images,name,owner,public,tracks"
        }

        r = SpotifyRequest("get", endpoint, params=params).send()

        playlist_info = r.json()
        meta = {
            "_id": "meta",
            "name": playlist_info.get("name"),
            "followers": playlist_info["followers"].get("followers"),
            "id": playlist_info.get("id"),
            "url": playlist_info["external_urls"].get("spotify"),
            "images": playlist_info.get("images"),
            "total_tracks":playlist_info["tracks"].get("total"),
            "public": playlist_info.get("public"),
            "user_id": self.user_id,
            "updated_at": datetime.datetime.now()
        }

        return {
            "meta": meta,
            "tracks": playlist_info.get("tracks")
        }
    
    
    def __get_song_id_set(self, tracks):
        """Helper function to convert a playlist's 
        songs into a set of the songs spotify id.

        :param tracks: Songs belonging to a playlist
        :type tracks: List of dicts
        :return: A set of all the songs id's
        :rtype: set
        """

        songs_set = set()
        for track in tracks:
            songs_set.add(track["track"]["id"])

        return songs_set
    

    def __update_mongo_playlist(self, current_tracks): # TODO: Return??
        """Updates the playlists' mongo collection based off
        the most recently pulled tracks from user's spotify.

        :param current_tracks: Most recent pull of playlists' tracks
        :type current_tracks: list of dicts
        """

        original_track_ids = self.__get_song_id_set(self.track_docs)
        most_recent_track_ids = self.__get_song_id_set(current_tracks)

        add_tracks = []
        delete_tracks = []

        modified_track_ids = original_track_ids.symmetric_difference(most_recent_track_ids)
        
        # Divy Up songs into correct 'action' - Add/Delete
        for id in modified_track_ids:

            if id in original_track_ids:
                delete_tracks.append(id)

            else:
                # Even though this loop will really only hit the 
                # first couple indices, its best not too nest. -- ??
                for track in current_tracks:
                    if track["track"]["id"] == id:
                        add_tracks.append(track)
                        break
        
        try:
            #TODO: Handle db operations better -- ensure it was added
            if (len(add_tracks) >= 1):
                self.PLAYLIST_COLLECTION.insert_many(add_tracks)

            if (len(delete_tracks) >= 1):
                self.PLAYLIST_COLLECTION.delete_many({"track.id": {"$in": delete_tracks}})
            
            print(f"Playlist {self.id} updated for user {self.user_id}... Deleted: {len(delete_tracks)} Added: {len(add_tracks)} ")
        except Exception as e:
            print("Error adding tracks to playlist:", e)


    def __modify_playlist(self, playlist, type="update"):
        """The meat and potatoes for modifying a playlist.
        Handles the updating of playlists' mongo collection 
        with the most recently pulled tracks and meta information.
        As well as, updating the objects properties with the most
        recent information.

        Batch Mode

            - False: An "update". Will pull all new current tracks and compare
            to the last updated list and will only add/delete the
            neccesary tracks.

            - True: A "fresh start". Will push to the playlists mongo collection
            in batches of 50. This is a straight add with no deduping, hence used
            in cases when the collection is empty for front-end user experience,
            purposes.

        :param playlist: If modifying a regular playlist
        a dict containing the meta information and first
        round of tracks for a regular playlist.
        :type playlist: dict | None if 'Liked Songs'
        :param type: Flag for batch mode, defaults to "update"
        :type type: str, optional
        """

        url = "https://api.spotify.com/v1/me/tracks?limit=50" # Default - Liked Songs

        current_tracks = []
        done = False
        meta = False
        
        batch = False if type == "update" else True # NOTE: Batch Mode

        if playlist:
            self.meta = playlist.get("meta")
            self.total_tracks = playlist["tracks"].get("total", self.total_tracks)
            
            url = playlist["tracks"].get("next")
            if not url:
                done = True

            tracks = self.__get_audio_features(playlist["tracks"].get("items"))
            if batch:
                self.track_docs += tracks
                self.PLAYLIST_COLLECTION.insert_many(tracks)
            else:
                current_tracks += tracks

        while not done:

            r = SpotifyRequest("get", url).send()

            data = r.json()

            if not playlist and not meta:
                self.meta = self.__liked_songs_meta(data.get("total", self.total_tracks))
                meta = True

            url = data.get("next", None)
            if not url:
                done = True

            tracks = self.__get_audio_features(data.get("items"))
            if batch:
                current_tracks = tracks
                self.track_docs += current_tracks
                self.PLAYLIST_COLLECTION.insert_many(current_tracks)
            else:
                current_tracks += tracks

        if not batch:
            self.__update_mongo_playlist(current_tracks)
            self.track_docs = current_tracks

        self.PLAYLIST_COLLECTION.update_one({"_id": "meta"}, {"$set": self.meta}, upsert=True)
        self.total_tracks = len(self.track_docs)
