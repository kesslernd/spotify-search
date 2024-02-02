This is a basic, standalone class implementation of the Spotify search API. It has the ability to search by each type
- album
- artist
- playlist
- track
- show
- episode
- audiobook

Right now, OAuth isn't implemented, so it's just based off of the CLIENT_ID and CLIENT_SECRET. Those are set when initializing the class, but that could probably be improved by pulling it from your environment

Whenever a search is performed, the class will check if it needs to get / refresh the access token, padded by 5 seconds to try to avoid race conditions between when the condition was checked vs when the API actually gets called.

Since I'm not using any SSO or OAuth, i'm not using the refresh token endpoint and instead just grabbing a new access token assuming that class lives long enough to time out the token (1 hour)

Usage:
```
CLIENT_ID = '<YOUR CLIENT ID>'
CLIENT_SECRET = '<YOUR CLIENT SECRET>'

client = SpotifySearchApiClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

artists = client.search_artists('Copeland')
albums = client.search_albums('Beneath Medicine Tree')
playlists = client.search_playlists('workout')
tracks = client.search_tracks('Mr. Brightside')
episodes = client.search_episodes('cool episode')
audiobooks = client.search_audiobooks('The Dark Tower')
```
