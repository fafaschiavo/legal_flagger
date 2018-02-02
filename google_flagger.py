from googlesearch import search

problematic_srings = [
'itunes',
'spotify',
'deezer'
]

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


print check_google_search('Farshad Kazemi', 'Kabouse Asheghi')

# Search of artist
# Search of release name