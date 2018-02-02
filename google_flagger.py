from googlesearch import search

problematic_srings = [
'itunes',
'spotify',
'deezer'
]

for url in search('Bad Guy (Feat. Jenocia X)', tld='com', lang='es', stop=5):
    print url

# Search of artist
# Search of release name