import datetime
import time

from flask_login import current_user
from pymongo import MongoClient
import requests

from spotify_visualizer.blueprints.spotify.helpers.user import get_access_token, refresh_access_token
from spotify_visualizer.helpers.spotify_api import SpotifyRequest


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

        mongo = MongoClient()
        self.PLAYLIST_COLLECTION = mongo[str(self.user_id)][str(self.id)]

        if not self.id:
            self.name = "Liked Songs"
            self.PLAYLIST_COLLECTION = mongo[str(self.user_id)]["liked_songs"]
            
    
        self.tracks = list(self.PLAYLIST_COLLECTION.find({"_id": {"$ne": "meta"}})) 
        self.total_tracks = len(self.tracks)

        if self.total_tracks == 0:
            self.tracks = []

        if source == "spotify":
            self.update_playlist_songs()

    
    def update_playlist_songs(self, type="update"):
        """Entry point into updating the playlist.

        :param type: Whether to use batch mode or not, defaults to "update"
        :type type: str, optional
        """

        if self.total_tracks == 0:
            type="batch"

        playlist = None
        if self.id: # Not liked songs
            playlist = self._playlist_meta()


        if self.debug:
            print(f"Playlist Update Type: {type}")

        self._modify_playlist(playlist=playlist, type=type)


    def delete_playlist():
        pass


    def get_analytics():
        pass


    def _liked_songs_meta(self, total_tracks):
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


    def _playlist_meta(self):
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
            "user_id": self.user_id,
            "updated_at": datetime.datetime.now()
        }

        return {
            "meta": meta,
            "tracks": playlist_info.get("tracks")
        }
    
    
    def _get_song_id_set(self, tracks):
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
    

    def _update_mongo_playlist(self, current_tracks): # TODO: Return??
        """Updates the playlists' mongo collection based off
        the most recently pulled tracks from user's spotify.

        :param current_tracks: Most recent pull of playlists' tracks
        :type current_tracks: list of dicts
        """

        original_track_ids = self._get_song_id_set(self.tracks)
        most_recent_track_ids = self._get_song_id_set(current_tracks)

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


    def _modify_playlist(self, playlist, type="update"):
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
            in batches of 100. This is a straight add with no deduping, hence used
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

            tracks = playlist["tracks"].get("items")
            if batch:
                self.tracks += tracks
                self.PLAYLIST_COLLECTION.insert_many(tracks)
            else:
                current_tracks += tracks

        while not done:

            r = SpotifyRequest("get", url).send()

            data = r.json()

            if not playlist and not meta:
                self.meta = self._liked_songs_meta(data.get("total", self.total_tracks))
                meta = True

            url = data.get("next", None)
            if not url:
                done = True

            if batch:
                current_tracks = data.get("items")
                self.tracks += current_tracks
                self.PLAYLIST_COLLECTION.insert_many(current_tracks)
            else:
                current_tracks += data.get("items")

        if not batch:
            self._update_mongo_playlist(current_tracks)
            self.tracks = current_tracks

        self.PLAYLIST_COLLECTION.update_one({"_id": "meta"}, {"$set": self.meta}, upsert=True)
        self.total_tracks = len(self.tracks)
     