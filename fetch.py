import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# auth stuff
with open("id.txt", "r") as id_file:
    client_id = id_file.read().strip()

with open("secret.txt", "r") as secret_file:
    client_secret = secret_file.read().strip()


ccm = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=ccm)


with open("playlist.txt", "r") as playlist_file:
    playlist_id = playlist_file.read().strip()

pl = sp.playlist_items(playlist_id=playlist_id, fields=["next, items(track(album(images(url))))"])

art = pl["items"]
while pl["next"]:
    pl = sp.next(pl)
    art.extend(pl["items"])

art = [track["track"]["album"]["images"][0]["url"] for track in art]

print(len(art))

art = set(art)
print(len(art))

with open("out.txt", "w") as f:
    f.write(str(art))

for path in art:
    resp = requests.get(path)
    resp.raise_for_status()
    path: str
    name = path.split("/")[-1]
    with open(f"jpegs/{name}.jpg", "wb") as jpg:
        jpg.write(resp.content)
