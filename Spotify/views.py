from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Create your views here.
def search(request):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="930becb21aff4a83abaeb84f48bdb076",
                                                               client_secret="d4d89c0ab5194e85ba03a0aacc83e3dc"))

    if request.method == 'POST':
        print("yes")
        artist = request.body.decode('utf-8')
        print(artist)

        results = sp.search(q=artist, limit=20)
        for idx, track in enumerate(results['tracks']['items']):
            print(idx, track['name'])

    return render(request,"Spotify/spotify_view.html")
