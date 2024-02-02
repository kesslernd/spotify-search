import requests
import json
import time

# 401 errors
class SpotifyTokenExpiredException(Exception):
    pass

# 403 errors
class SpotifyBadOAuthException(Exception):
    pass

# 429 errors
class SpotifyRateLimitExceededException(Exception):
    pass


class SpotifySearchApiClient:
    DEFAULT_LIMIT = 5

    ARTIST = 'artist'
    ALBUM = 'album'
    PLAYLIST = 'playlist'
    TRACK = 'track'
    SHOW = 'show'
    EPISODE = 'episode'
    AUDIOBOOK = 'audiobook'

    client_id = ''
    client_secret = ''
    access_token = ''
    token_type = ''
    token_exprires_at = 0
    token_end = None
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    # check if we need to refresh the access token
    def check_token(self):
        # pad the timing a bit so we dont run into a race condition
        if not self.token_exprires_at or self.token_exprires_at > int(time.time()) - 5:
            self.set_access_token()

    # get the access token for other API calls
    def set_access_token(self):
        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(auth_url, data=data, headers=headers)
        self.validate_response(response)
        data = json.loads(response.content)
        self.access_token = data['access_token']
        self.token_type = data['token_type']
        self.exprires_in = data['expires_in']
        self.token_end = int(time.time()) + self.token_exprires_at

    # call the search api
    def search(self, type, input, limit, market, offset):
        self.check_token()

        search_limit = limit if limit else self.DEFAULT_LIMIT
        market = market if market else ''
        offset = offset if offset else 0

        url = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        data = {
            'q': input,
            'type': type,
            'limit': search_limit,
        }
        response = requests.get(url, params=data, headers=headers)
        self.validate_response(response)
        data = json.loads(response.content)
        return data
    
    # throw an exception if we need to based off the http response code
    def validate_response(response):
        if response.status_code == 200:
            pass
        if response.status_code == 401:
            raise SpotifyTokenExpiredException(message=response.message)
        if response.status_code == 403:
            raise SpotifyBadOAuthException(message=response.message)
        if response.status_code == 429:
            raise SpotifyRateLimitExceededException(message=response.message)
        
    def search_artists(self, input, limit=None, market='', offset=None):
        data = self.search(type=self.ARTIST, input=input, limit=limit, market=market, offset=offset)
        return [d for d in data['artists']['items']]

    def search_albums(self, input, limit=None, market='', offset=None):
        data = self.search(type=self.ALBUM, input=input, limit=limit, market=market, offset=offset)
        return [d for d in data['albums']['items']]

    def search_playlists(self, input, limit=None, market='', offset=None):
        data = self.search(type=self.PLAYLIST, input=input, limit=limit, market=market, offset=offset)
        return [d for d in data['playlists']['items']]
    
    def search_tracks(self, input, limit=None, market='', offset=None):
        data = self.search(type=self.TRACK, input=input, limit=limit, market=market, offset=offset)
        return [d for d in data['tracks']['items']]
    
    def search_shows(self, input, limit=None, market='', offset=None):
        data = self.search(type=self.SHOW, input=input, limit=limit, market=market, offset=offset)
        return [d for d in data['shows']['items']]

    def search_episodes(self, input, limit=None, market='', offset=None):
        data = self.search(type=self.EPISODE, input=input, limit=limit, market=market, offset=offset)
        return [d for d in data['episodes']['items']]
    
    def search_audiobooks(self, input, limit=None, market='', offset=None):
        data = self.search(type=self.AUDIOBOOK, input=input, limit=limit, market=market, offset=offset)
        return [d for d in data['audiobooks']['items']]


CLIENT_ID = '<YOUR CLIENT ID>'
CLIENT_SECRET = '<YOUR CLIENT SECRET>'

client = SpotifySearchApiClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

artists = client.search_artists('Copeland')
albums = client.search_albums('Beneath Medicine Tree')
playlists = client.search_playlists('workout')
tracks = client.search_tracks('Mr. Brightside')
episodes = client.search_episodes('cool episode')
audiobooks = client.search_audiobooks('The Dark Tower')