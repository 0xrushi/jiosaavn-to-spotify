import sys
import spotipy
import yaml
import spotipy.util as util
from pprint import pprint
global sp
global user_config

from Download import processPlaylist

def load_config():
    global user_config
    stream = open('config.yaml')
    user_config = yaml.load(stream)
    pprint(user_config)
def get_top_songs_for_artist(artist,track, song_count=1):
    #print(track)
    song_ids = []
    #artist_results = sp.search(q='artist:' + artist, type='artist', limit=1)
    artist_results = sp.search(q='track:' + track + ' artist:'+ artist,limit=1)
    pprint(artist_results['tracks']['total']==0)
    if not artist_results['tracks']['total'] == 0:
        artist_id = artist_results['tracks']['items'][0]['id']
        pprint(artist_id)
        artist_results_len=len(artist_results['tracks']['items'])
        #print(artist_results['tracks']['items'])
        for x in range(0, artist_results_len if song_count > artist_results_len else song_count ):
            song_ids.append(artist_results['tracks']['items'][x]['id'])
            # pprint(artist_top_tracks['tracks'][x])
        print(str(len(song_ids)) + ' songs found - ' + artist)
    else:
        print('Artist not found - ' + artist)
        # pprint(song_ids)
    return song_ids

def get_wacken_tracks(tracks,artists):
    all_track_ids = []
    for i, current_artist in enumerate(artists):
        print(current_artist)
        api_track_add_limit = 100
        top_song_limit_per_artist = 2
        top_artist_songs = get_top_songs_for_artist(current_artist,tracks[i], top_song_limit_per_artist)
        if len(top_artist_songs):
            all_track_ids.extend(top_artist_songs)
        if len(all_track_ids)+ top_song_limit_per_artist > api_track_add_limit or (i == len(artists)-1 and len(all_track_ids)):
            sp.user_playlist_add_tracks(user=user_config['username'], playlist_id=user_config['playlist_id'], tracks=all_track_ids)
            all_track_ids = []
if __name__ == '__main__':
    load_config()
    plink = input("Enter Playlist URL: ")
    tracks, artists = processPlaylist(plink)
    print(tracks) 
    print(artists)
    
    token = util.prompt_for_user_token(user_config['username'], scope='playlist-modify-private,playlist-modify-public', client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])
    if token:
        sp = spotipy.Spotify(auth=token)
        get_wacken_tracks(tracks,artists)
    else:
        print ("Can't get token for", user_config['username'])