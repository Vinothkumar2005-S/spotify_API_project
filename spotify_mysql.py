import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pymysql

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='8a7b7534199a4f2086bd58066fc407ca',  # Replace with your Client ID
    client_secret='0a8762ae8a124aef9f60139b456f60a9'  # Replace with your Client Secret
))

# MySQL Database Connection
db_config = {
    'host': 'localhost',           # Change to your MySQL host
    'user': 'root',       # Replace with your MySQL username
    'password': '2005',   # Replace with your MySQL password
    'database': 'spotify_db'       # Replace with your database name
}

# Connect to the database
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Read track URLs from file
file_path = "E:\\data sets\\spotify_data_analytics-main\\track_urls.txt"
with open(file_path, 'r') as file:
    track_urls = file.readlines()

# Process each URL
for track_url in track_urls:
    track_url = track_url.strip()  # Remove any leading/trailing whitespace
    try:
        # Extract track ID from URL
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

        # Fetch track details from Spotify API
        track = sp.track(track_id)

        # Extract metadata
        track_data = {
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration (minutes)': track['duration_ms'] / 60000
        }

        # Insert data into MySQL
        insert_query = """
        INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration (minutes)']
        ))
        connection.commit()

        print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']}")

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

# Close the connection
cursor.close()
connection.close()

print("All tracks have been processed and inserted into the database.")
