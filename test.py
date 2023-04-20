import requests
client_access_token = "TXCac-UW7QvkqNWPN5Ok7uY1PgDcRkFDyYWw1PonphwJV81dXUdZ3Xg3o-KAX8EJ"

search_term = "Dean Blunt - The Narcissist "

url = "http://api.genius.com/search?q=" + search_term + "&access_token=" + client_access_token

response = requests.get(url)

def get_first_song_image(response):
    for hit in response.json()["response"]["hits"]:
        if hit["type"] == "song":
            return hit["result"]["song_art_image_thumbnail_url"]

print(get_first_song_image(response))