import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pickle.load(open('movie_dir.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('simi.pkl', 'rb'))


def fetch_post(movie_id):
    response = requests.get(
        url="https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    print(data)
    # st.text(data) #debug
    # Ensure poster path exists
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        # Fallback to a placeholder image if not available
        return "https://via.placeholder.com/500"


def recommend(movie):
    movie_idx = movies['title'][movies['title'] ==
                                movie].index[0]  # matching the title to index
    # finding distances of given movie in verctor simmilrization we created

    distances = similarity[movie_idx]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6]  # sorting the less distces top 5 movies and recommending it

    recommend_movies = []
    recommend_mov_post = []

    for i in movie_list:

        # trying to fetch posters  #api key :: 84ad372562be05321a878c0d6c3c1653
        movie_id = movies.iloc[i[0]].movie_id

        # recommending the movie
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_mov_post.append(fetch_post(movie_id))

    return recommend_movies, recommend_mov_post


st.title('Movie Reccommder system')

selected_mo = st.selectbox(
    'Select Movies : ',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_mo)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(posters[0])
        st.text(names[0])
    with col2:
        st.image(posters[1])
        st.text(names[1])
    with col3:
        st.image(posters[2])
        st.text(names[2])

    col4, col5 = st.columns(2)
    with col4:
        st.image(posters[3])
        st.text(names[3])
    with col5:
        st.image(posters[4])
        st.text(names[4])
