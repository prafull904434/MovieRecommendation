import streamlit as st
import pickle
import requests
from PIL import Image
import os
from dotenv import load_dotenv

api_key=os.environ.get('api_key')
load_dotenv()

df=pickle.load(open('movies.pkl','rb'))
movies_list=df['title'].values

similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=71bdf77c281ab58ac1a0371b5ed7682c&language=English')
    data=response.json()
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index=df[df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=df.iloc[i[0]]['id']
        recommended_movies.append(df.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
        # print(i[0], df.iloc[i[0]]['title'])
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommendation System")

selectedMovieName = st.selectbox(
    'Select a movie you would like to watch',
    movies_list)

# st.write('You selected:', option)
if st.button('Recommend'):
    names, posters=recommend(selectedMovieName)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    