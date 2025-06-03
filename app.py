import pickle
import streamlit as st
import requests

# --- Poster Fetch Function ---
def fetch_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Image"

# --- Recommend Function ---
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# --- Streamlit App ---
st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))  # this has 'id' column, not 'movie_id'
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Dropdown
list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", list)

# Button click
if st.button('Show Recommendation'):
    recommended_names, recommended_posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_names[0])
        st.image(recommended_posters[0])
    with col2:
        st.text(recommended_names[1])
        st.image(recommended_posters[1])
    with col3:
        st.text(recommended_names[2])
        st.image(recommended_posters[2])
    with col4:
        st.text(recommended_names[3])
        st.image(recommended_posters[3])
    with col5:
        st.text(recommended_names[4])
        st.image(recommended_posters[4])
