from spotify_visualizer.field_names import CAMELOT

class Track():

    def __init__(self, doc, debug=False):

        self.debug = debug
        
        track = doc.get("track")
        self.id = track.get("id")
        self.spotify_url = track["external_urls"].get("spotify")
        self.name = track.get("name")
        self.__set_artists(track.get("artists"))
        self.duration_ms = track.get("duration_ms")

        audio_features = doc.get("audio_features")
        self.key = audio_features.get("key")
        self.mode = audio_features.get("mode")
        self.bpm = round(audio_features.get("tempo")) # Closest Integer
        self.__set_camelot()

        if self.debug:
            print("Track created:", self.name)


    def get_genre(self):
        pass


    def __set_camelot(self):
        """Helper function that uses spotify provided data on a 
        tracks tempo and key in order to generate the camelot
        key notation for the track and set it to the 'camelot_notation'
        property.

        The tracks 'key' and 'mode' properties need to be set before calling
        this function.
        """

        note = CAMELOT.PITCH_CLASS.get(str(self.key))

        # Major
        if self.mode == 1:
            self.camelot_notation = CAMELOT.MAJOR.get(note)
        # Minor
        else:
            self.camelot_notation = CAMELOT.MINOR.get(note)


    def __set_artists(self, artists):
        """Helper function that iterates through the tracks
        api response artist array and sets the 'artists' property
        with the data found.

        :param artists: 'artists' array that is apart of the track 
        object found in a tracks doc.
        :type artists: array of dicts
        """

        self.artists = []

        for artist in artists:
            self.artists.append({
                "name": artist.get("name"),
                "id": artist.get("id"),
                "spotify_url": artist["external_urls"].get("spotify"),
                "api_url": artist.get("href")
            })




