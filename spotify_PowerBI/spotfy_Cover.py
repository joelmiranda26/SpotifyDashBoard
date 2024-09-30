import requests
import base64
import pandas as pd

# Replace with your own Spotify credentials
client_id = '123005656bdf41358538ed5ee2a3958a'
client_secret = '0cca7a099d814de59e7105307dca3730'

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    token = response.json()['access_token']
    return token

# Function to search Spotify for track and get album cover URL
def get_album_cover_url(track_name, artist_name, token):
    search_url = f'https://api.spotify.com/v1/search?q=track:{track_name}%20artist:{artist_name}&type=track'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        results = response.json()
        if results['tracks']['items']:
            album_cover_url = results['tracks']['items'][0]['album']['images'][0]['url']
            return album_cover_url
    return None

# Load your Spotify dataset
file_path = 'spotify.csv'
spotify_data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Add a new column for album cover URLs
spotify_data['album_cover_url'] = None

# Get Spotify API token
token = get_spotify_token(client_id, client_secret)

# Loop through each row in the dataset and fetch album cover URL
for index, row in spotify_data.iterrows():
    track_name = row['track_name']
    artist_name = row['artist(s)_name']
    
    # Fetch album cover URL from Spotify API
    album_cover_url = get_album_cover_url(track_name, artist_name, token)
    
    # Update the dataset
    spotify_data.at[index, 'album_cover_url'] = album_cover_url

# Save the updated dataset to a new CSV file
spotify_data.to_csv('updated_spotify_data.csv', index=False)

print("Album cover URLs added successfully!")
