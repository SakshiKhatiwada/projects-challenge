import streamlit as st
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")
BASE_URL = "https://api.themoviedb.org/3/movie"
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/original' #https://image.tmdb.org/t/p/original/[poster_path]

movies_df = pickle.load(open("Project1_Movie_Recommender_System/movies.pkl", "rb"))
similarity = pickle.load(open("Project1_Movie_Recommender_System/similarity.pkl", 'rb'))
movies_list = movies_df['title'].values

def fetch_poster(movie_id):
    URL = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
    "accept":"application/json",
    "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}"
    }
    response = requests.get(URL,headers=headers )
    data = response.json()
    # print(data['posters'][0]['file_path'])
    return IMAGE_BASE_URL + data['posters'][0]['file_path']
    
def recommend_movie(movie):  
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        similar_movies = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = [] 
        recommended_movies_posters = [] 
        
        for i in similar_movies:
            # print(movies_df.iloc[i[0]].title)
            recommended_movies.append(movies_df.iloc[i[0]].title)
            movie_id = movies_df.iloc[i[0]]['id'] # fetch id from the row
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    
#  --------

st.title("Movie Recommender System")

selected_movie = st.selectbox("What movie did you already see?", movies_list) # 2nd argument is options

if st.button("Recommend"):
    selected_movie_index = movies_df.loc[movies_df['title'] == selected_movie, 'id'].iloc[0]
    selected_movie_poster = fetch_poster(selected_movie_index)
    
    cola, colb = st.columns(2)
    with cola:
        st.image(selected_movie_poster)
    with colb:
        st.write("You Loved this movie, scroll down for Similar Movies")
    # recommended movies
    
    st.header("Try these movies now:")
    recommendations, posters = recommend_movie(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(recommendations[0])
        st.image(posters[0])

    with col2:
        st.write(recommendations[1])
        st.image(posters[1])

    with col3:
        st.write(recommendations[2])
        st.image(posters[2])
        
    with col4:
        st.write(recommendations[3])
        st.image(posters[3])
        
    with col5:
        st.write(recommendations[4])
        st.image(posters[4])
    
