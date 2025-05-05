import mysql.connector
from spotipy import SpotifyClientCredentials
import pandas as pd 
import spotipy
import matplotlib.pyplot as plt
import re
import pymysql
from sqlalchemy import create_engine

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id = '8a7b7534199a4f2086bd58066fc407ca',
    client_secret = '0a8762ae8a124aef9f60139b456f60a9'))

track_url = "https://open.spotify.com/track/003vvx7Niy0yvhvHt4a68B"

track_id = re.search(r'track/([a-zA-Z0-9]+)',track_url).group(1)

track = sp.track(track_id)
print(track)


# extract metadata 
track_data = {
    'track_name':track['name'],
    'Artist':track['artists'][0]['name'],
    'Album':track['album']['name'],
    'popularity':track['popularity'],
    'Duration (minutes)':track["duration_ms"]/60000
}

# display metadata 
print(f"\track_name :{track_data['track_name']}")
print(f"Artist:{track_data['Artist']}")
print(f"Album:{track_data['Album']}")
print(f"Popularity:{track_data['popularity']}")
print(f"Duration:{track_data['Duration (minutes)']:.2f} minutes")

df = pd.DataFrame([track_data])
print("\nTrack data as Dataframe")
print(df)

df.to_csv('spotify_track_data.csv',index= False)

# visualisations by matplotlib

features = ['populartity','Duration (minutes)']
values = [track_data['popularity'],track_data['Duration (minutes)']]

plt.figure(figsize=(8,5))
plt.bar(features,values,color = 'skyblue',edgecolor = 'red')
plt.title(f"track metadata for '{track_data['track_name']}")
plt.ylabel('value')
plt.show()


engine_mysql = create_engine("mysql+pymysql://root:2005@127.0.0.1:3306/spotify_db")

try:
    create_engine
    print("engine sucessfully active")
except:
    print("unable to connect")

df.to_sql('spotify_db',con=engine_mysql,if_exists='append' , index= False)


## file handling 
