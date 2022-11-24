import streamlit as st
import pandas as pd
import re

st.write("""
# Spotify Song Recommender 🎧
This app recommends 10 tracks based on your favorite songs.
# """)

tracks = pd.read_csv('data.csv')

popularity_val = st.slider('Slide to adjust track popularity', min_value=0, max_value=70)

tracks = tracks[tracks.popularity > popularity_val]

# taking user input for songs
spotify_url = st.text_input('Enter comma-separated Spotify URLs of your favorite songs:')

id_pre = spotify_url.strip().split(',')


if spotify_url: 
    # https://open.spotify.com/track/0fUFpbQsTXojtPfKasNfXZ?si=b38c67ea5a6641d2
    # need regex to extract song id from url
    ids = [re.search('track/(.*)\?', url).group(1) for url in id_pre]

    # search the specified ids in this dataset and get the tracks
    favorites = tracks[tracks.id.isin(ids)]

    # code to sort find out the maximum occuring cluster number according to user's favorite track types
    cluster_numbers = list(favorites['type'])
    clusters = {}
    for num in cluster_numbers:
        clusters[num] = cluster_numbers.count(num)

    # sort the cluster numbers and find out the number which occurs the most

    user_favorite_cluster = [(k, v) for k, v in sorted(clusters.items(), key=lambda item: item[1])][0][0]

    #print('\nFavorite cluster:', user_favorite_cluster, '\n')

    # finally get the tracks of that cluster
    suggestions = tracks[tracks.type == user_favorite_cluster]

   #now print the first 5 rows of the data frame having that cluster number as their type
    st.dataframe(suggestions[['name','uri']].sample(10))

    # play an audio clip of the song
    #st.audio("", format='audio/mp3')
    st.balloons()
