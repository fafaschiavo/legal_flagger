import acoustid
from googlesearch import search
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from os import listdir, walk
from os.path import isfile, join, isdir
import json
import pandas as pd

problematic_srings = [
'itunes',
'spotify',
'deezer'
]

mypath = './'

output_file = 'copyright_repport.txt'

CLIENT_APIKEY = 'tGyf3jN3PB'
USER_APIKEY = 'AxDKFSdxiv'

def check_fingerprint(audio_file):
	fingerprint_pair = acoustid.fingerprint_file(audio_file)
	results = acoustid.lookup(CLIENT_APIKEY, fingerprint_pair[1], fingerprint_pair[0])
	if len(results['results']) == 0:
		return None
	return results['results']

def check_google_search(artist_name, release_name):
	artist_name_flag = []
	for found_url in search(artist_name, tld='com', lang='es', stop=5):
		for problematic_sring in problematic_srings:
			if problematic_sring in found_url:
				artist_name_flag.append(found_url)

	if len(artist_name_flag) == 0:
		artist_name_flag = None

	release_name_flag = []
	for found_url in search(artist_name + ' ' + release_name, tld='com', lang='es', stop=5):
		for problematic_sring in problematic_srings:
			if problematic_sring in found_url:
				release_name_flag.append(found_url)

	if len(release_name_flag) == 0:
		release_name_flag = None

	return artist_name_flag, release_name_flag

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

def add_to_report(release_name, text_to_add):
	if os.path.exists(output_file):
		append_write = 'a' # append if already exists
	else:
		append_write = 'w' # make a new file if not
	report_file = open(output_file,append_write)
	report_file.write(text_to_add + '\n')
	report_file.close()

total_analysed_so_far = 0
number_of_flags = 0
flags_per_release = {}
my_folders = [f for f in listdir(mypath) if isdir(join(mypath, f))]
for folder in my_folders:
	total_analysed_so_far = total_analysed_so_far + 1
	print '-------------------------'
	print 'Now checking - ' + folder
	print 'Total checked - ' + str(total_analysed_so_far) + '/' + str(len(my_folders))

	df = pd.read_csv(mypath + folder + '/metadata.csv')
	release_name = df['Release Title'][0]
	artist_name = df['Artists'][0]

	google_artist_name_flag, google_release_name_flag = check_google_search(artist_name, release_name)
	spotify_artist_results, spotify_release_results = check_spotify(artist_name, release_name)

	if google_artist_name_flag is not None:
		number_of_flags = number_of_flags + 1
		if folder in flags_per_release:
			flags_per_release[folder] = flags_per_release[folder] + 1
		else:
			flags_per_release[folder] = 1
		amount_of_matches = len(google_artist_name_flag)
		result_json = json.dumps(google_artist_name_flag, ensure_ascii=False)
		text_to_add = '''
		=====================================================================
		%s - Was flagged by the Google artist name with %d matches
		\n\n
		Following a JSON with the found matches:
		\n
		%s
		''' % (folder, amount_of_matches, result_json)
		text_to_add = text_to_add.replace('	', '')
		add_to_report(folder, text_to_add)

	if google_release_name_flag is not None:
		number_of_flags = number_of_flags + 1
		if folder in flags_per_release:
			flags_per_release[folder] = flags_per_release[folder] + 1
		else:
			flags_per_release[folder] = 1
		amount_of_matches = len(google_release_name_flag)
		result_json = json.dumps(google_release_name_flag, ensure_ascii=False)
		text_to_add = '''
		=====================================================================
		%s - Was flagged by the Google release name with %d matches
		\n\n
		Following a JSON with the found matches:
		\n
		%s
		''' % (folder, amount_of_matches, result_json)
		text_to_add = text_to_add.replace('	', '')
		add_to_report(folder, text_to_add)

	if spotify_artist_results is not None:
		number_of_flags = number_of_flags + 1
		if folder in flags_per_release:
			flags_per_release[folder] = flags_per_release[folder] + 1
		else:
			flags_per_release[folder] = 1
		amount_of_matches = len(spotify_artist_results)
		result_json = json.dumps(spotify_artist_results, ensure_ascii=False)
		text_to_add = '''
		=====================================================================
		%s - Was flagged by the Spotify artist name with %d matches
		\n\n
		Following a JSON with the found matches:
		\n
		%s
		''' % (folder, amount_of_matches, result_json)
		text_to_add = text_to_add.replace('	', '')
		add_to_report(folder, text_to_add)

	if spotify_release_results is not None:
		number_of_flags = number_of_flags + 1
		if folder in flags_per_release:
			flags_per_release[folder] = flags_per_release[folder] + 1
		else:
			flags_per_release[folder] = 1
		amount_of_matches = len(spotify_release_results)
		result_json = json.dumps(spotify_release_results, ensure_ascii=False)
		text_to_add = '''
		=====================================================================
		%s - Was flagged by the Spotify release name with %d matches
		\n\n
		Following a JSON with the found matches:
		\n
		%s
		''' % (folder, amount_of_matches, result_json)
		text_to_add = text_to_add.replace('	', '')
		add_to_report(folder, text_to_add)

	audio_files = [f for f in listdir(mypath + '/' + folder) if '.mp3' in f]
	for audio_file in audio_files:
		fingerprint_result = check_fingerprint(mypath + '/' + folder + '/' + audio_file)
		if fingerprint_result is not None:
			number_of_flags = number_of_flags + 1
			if folder in flags_per_release:
				flags_per_release[folder] = flags_per_release[folder] + 1
			else:
				flags_per_release[folder] = 1
			amount_of_matches = len(fingerprint_result)
			result_json = json.dumps(fingerprint_result, ensure_ascii=False)
			text_to_add = '''
			=====================================================================
			%s - Was flagged by fingerprint with %d matches
			\n\n
			Following a JSON with the found matches:
			\n
			%s
			''' % (folder, amount_of_matches, result_json)
			text_to_add = text_to_add.replace('	', '')
			add_to_report(folder, text_to_add)

print '============================'
print 'Analysis done'
print 'Number of flags raised: ' + str(number_of_flags)
print '\n'
for release, flags in flags_per_release.iteritems():
	print release + ' - ' + str(flags) + '/5'
print '============================'