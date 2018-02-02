import acoustid

def check_fingerprint(audio_file):
	CLIENT_APIKEY = 'tGyf3jN3PB'
	USER_APIKEY = 'AxDKFSdxiv'

	fingerprint_pair = acoustid.fingerprint_file(audio_file)

	results = acoustid.lookup(CLIENT_APIKEY, fingerprint_pair[1], fingerprint_pair[0])
	if len(results['results']) == 0:
		return None
	return results



# audio_file = '7325e41189fa4027eb0d2b7c9bfd5b90298cf0c4.mp3'
audio_file = 'deep_purple_smoke_on_the_water.mp3'
results = check_fingerprint(audio_file)

if results is not None:
	for result in results['results']:
		print result['score']
else:
	print 'No results found'

# To install chromaprint - brew install chromaprint
# Or on ubuntu - sudo apt-get install libchromaprint-tools
# CLIENT_APIKEY = 'tGyf3jN3PB'
# USER_APIKEY = 'AxDKFSdxiv'