import sys
print(sys.executable)
import warnings
warnings.filterwarnings('ignore')

import pickle 
import streamlit as st
import pandas as pd
import requests


movies_set = pickle.load(open('movie_set.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_set)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f4b23bf84275e9cc787656b48e72e912&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['Title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].Movie_ID
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].Title)

    return recommended_movie_names,recommended_movie_posters

st.header("Popcorn Ready? Let's roll!")
selected_movie = st.selectbox(
    'Discover your next favorite movie',
(movies['Title'].values))

try:
    if st.button('Get Suggestions'):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        st.caption('Your next cinematic obsession could be among these top-rated choices')
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])

        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
        st.caption("Thank you for using Moviemate! :sunglasses:")
except:
    st.caption("Oops! {} is one of a kind.".format(selected_movie))
    st.caption("Thank you for using Moviemate! :sunglasses:")


# https://api.themoviedb.org/3/movie/{}/watch/providers?api_key=f4b23bf84275e9cc787656b48e72e912.format(Movie_ID)
