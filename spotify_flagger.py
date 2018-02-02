import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def check_spotify(artist_name, release_name):
	client_credentials_manager = SpotifyClientCredentials(client_id='319e6239680d43aa90eb8d4062815394', client_secret='8e6f5322cac94502a533cde0c8b628d7')
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	artist_results = sp.search(q=artist_name, type='artist')
	artist_results = artist_results['artists']['items']
	if len(artist_results) == 0:
		artist_results = None

	release_results = sp.search(q=artist_name + ' ' + release_name, type='album')
	release_results = release_results['albums']['items']
	if len(release_results) == 0:
		release_results = None

	return artist_results, release_results

print check_spotify('Steve Reason', 'I Dont Wanna Miss This')
print check_spotify('Razablade Real', 'Giberish')
print check_spotify('Deep Purple', 'Giberish')