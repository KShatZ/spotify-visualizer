from flask_login import UserMixin

from spotify_visualizer.helpers.spotify_api import SpotifyRequest


class User(UserMixin):
    """User class that is passed around as flask-logins
    'current_user'. Inherits from flask-logins UserMixin
    base class.

    :param UserMixin: flask-login base user class
    :type UserMixin: UserMixin
    """

    def __init__(self, user_doc):
        self.id = user_doc["_id"]
        self.username = user_doc["username"]

        if user_doc["spotify"]:
            self.spotify = user_doc["spotify"].get("user")
        else:
            self.spotify = None


    def get_total_tracks(self):
        """Hits Spotify API to retrieve
        total number of tracks a user has saved
        in the "Liked Songs" playlist.

        :return: The number of songs the current 
        user has saved
        :rtype: int
        """

        r = SpotifyRequest("get", "https://api.spotify.com/v1/me/tracks")

        data = r.send().json()
        return data.get("total")


    def get_playlists(self):
        """Returns information on all of the users'
        playlists.

        :return: List containing meta information on users'
        playlists
        :rtype: list of dics
        """
        
        user_playlists = []
        user_spotify_id = self.spotify.get("id")

        url = "https://api.spotify.com/v1/me/playlists?limit=50"

        done = False
        while not done:

            r = SpotifyRequest("get", url)
            data = r.send().json()

            url = data.get("next", None)
            if not url:
                done = True

            playlists = data.get("items")

            for playlist in playlists:

                playlist_owner = playlist["owner"].get("id")

                if playlist_owner == user_spotify_id:

                    images = playlist.get("images")
                    if len(images) == 0:
                        image = None
                    else:
                        image = images[0] # First image is the biggest

                    user_playlist = {
                        "id": playlist.get("id"),
                        "name": playlist.get("name"),
                        "image": image,
                        "public": playlist.get("public"),
                        "track_count": playlist["tracks"].get("total"),
                    }

                    user_playlists.append(user_playlist)

        return (user_playlists, len(user_playlists))
    

    def get_following_count(self):
        """Hit Spotify API to get the total
        number of artists the current user is 
        following.

        :return: The number of artists the user is following
        :rtype: int
        """
    
        r = SpotifyRequest("get", "https://api.spotify.com/v1/me/following?type=artist")
        data = r.send().json()

        total_count = data["artists"].get("total", "N/A")

        return total_count
    

    def get_profile_image(self):
        """Gets the largest user profile image url that exists.
        Spotify rotates url's for the profile image so need to utilze
        a getter to prevent a missing profile image.

        :return: The spotify url to the users profile image
        :rtype: str
        """

        profile_images = self.spotify.get("images")

        largest_size = 0
        index = None

        try:
            for i, image in enumerate(profile_images):
                image_size = image.get("height", 0)

                if image_size > largest_size:
                    largest_size = image_size
                    index = i

            return profile_images[index].get("url")
        
        except:
            return None
        