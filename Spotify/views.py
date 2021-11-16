from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Create your views here.
def search(request):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="930becb21aff4a83abaeb84f48bdb076",
                                                         client_secret="d4d89c0ab5194e85ba03a0aacc83e3dc"))
    track_name = []
    track_link = []

    if request.method == 'POST':
        artist = request.body.decode('utf-8')
        print(artist)

        results = sp.search(q=artist, limit=10)

        for idx, track in enumerate(results['tracks']['items']):
            track_name.append(track['name'])


            track_link.append(track['preview_url'])

        print(track_name)

        return render(request, "Spotify/show_view.html",{"track_name":track_name,
                                                            "track_link":track_link})

    return render(request,"Spotify/spotify_view.html")
