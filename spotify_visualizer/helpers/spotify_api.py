import time

from flask_login import current_user
import requests

from spotify_visualizer.blueprints.spotify.helpers.user import get_access_token, refresh_access_token
from spotify_visualizer.field_names import Status


class SpotifyRequest():
    """A wrapper for requests sent to the Spotify API. 
    Handles, nuances such as the authorization header, as 
    well as access token refreshing if needed.
    """

    def __init__(self, method, url, params=None, headers={}, debug=False):
        """SpotifyRequest constructor

        :param method: HTTP verb, at the moment can only 
        be GET or POST.
        :type method: str
        :param url: Spotify API url to send the request to.
        Does not work with the authentication URL's at the moment.
        :type url: str
        :param params: URL query params, defaults to None
        :type params: dict, optional
        :param headers: Headers to add to the request
        the 'send' method handles adding the 'Authentication'
        header so you do not need to set this one as it will
        be overwritten anyways. defaults to {}
        :type headers: dict, optional
        """

        self.debug = debug

        #TODO - Ensure spotify url, prob some other checks too

        self.request_count = 0
        self.url = url
        self.method = method.lower()       
        self.params = params
        self.headers = headers
        
        self.user_id = current_user.id
        self.access_token = get_access_token(self.user_id)


    def send(self):
        """Main function to call in order to send a request.
        Handles sending the specified Spotify API request and any
        refreshing of access tokens or other issues.

        :return: Response from spotify
        :rtype: Response Object
        """
        
        METHODS = ["get", "post"]

        #TODO - Better Handling
        if self.method not in METHODS: 
            print(f"Incorrect method ({self.method}) provided...")
            return 
    
        #TODO - Better Handling, Field Name MAX_REQUEST
        if self.request_count > 4: 
            print("Too many requests sent...")
            return

        self.headers["Authorization"] = f"Bearer {self.access_token}"
        
        if self.debug:
            print(f"Sending {self.method} request to {self.url} for user {self.user_id}")
            print(f"Params: {self.params}")
            print(f"Headers: {self.headers}")

        try:
            if self.debug:
                print(f"Sending {self.method} request to {self.url} for user {self.user_id}")
                print(f"Params: {self.params}")
                print(f"Headers: {self.headers}")
            
            r = requests.request(self.method, self.url, params=self.params, headers=self.headers, timeout=60)

            if self.debug:
                print("Response Status Code:", r.status_code)
                
        except Exception as e: # TODO: Better Handling
            print(f"SpotifyRequest: Issue sending request to API \n The error: {e}")
        
        if r.status_code == Status.UNAUTHORIZED:
            print(f"401: Request to {self.url} for user {self.user_id}")
            self.request_count += 1
            return self._handle_refresh()

        if r.status_code == Status.SERVER_ERROR:
            print(f"500: Request to {self.url} for user {self.user_id}")
            self.request_count += 1
            return self._timeout(2)

        return r

    
    def _handle_refresh(self):
        """Refreshes the user's access token and
        sends the request again

        :return: send() request function
        :rtype: func
        """

        if self.debug:
            print(f"Refreshing access for {self.user_id}")

        self.access_token = refresh_access_token(self.user_id)

        # TODO
        if not self.access_token:
            print("There was an issue with refreshing access token")
            return

        return self.send()


    def _timeout(self, seconds):
        """A helper function to sleep for a
        number of seconds before sending request
        again.

        :return: send() request function
        :rtype: func
        """

        if self.debug:
            print(f"Time out for {seconds} seconds")
            
        time.sleep(seconds)
        return self.send()
