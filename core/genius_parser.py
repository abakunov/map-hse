import requests


def get_song_image(artist, name, client_access_token):
    url = "http://api.genius.com/search?q=" + artist + ' - ' + name + "&access_token=" + client_access_token
    response = requests.get(url)

    for hit in response.json()["response"]["hits"]:
        if hit["type"] == "song":
            return hit["result"]["song_art_image_thumbnail_url"]
