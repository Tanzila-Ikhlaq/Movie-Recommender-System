
import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=da22878a12d0f70aece5a755687f0af7")
    data=response.json()
    return "http://image.tmdb.org/t/p/w500/" + data["poster_path"]

# Load your movie data from the pickle file
movies_data = pickle.load(open("movie_dict.pkl", "rb"))
similarity=pickle.load(open("similarity.pkl","rb"))

# Create a DataFrame from the loaded data
df = pd.DataFrame(movies_data)

def recomend(x):
    x_index=df[df["title"]==x].index[0]
    distances=similarity[x_index]
    x_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recomended_x=[]
    recomended_x_posters=[]
    for i in x_list:
        movie_id=df.iloc[i[0]].movie_id
        recomended_x.append(df.iloc[i[0]].title)
        #fetching poster from API
        recomended_x_posters.append(fetch_poster(movie_id))
    return recomended_x,recomended_x_posters

st.title("Movie Recommender System")

# Create a selectbox for choosing a genre
movie_name = st.selectbox("Choose a movie", df["title"].values)

if st.button("Recomend"):
    names,posters=recomend(movie_name)
    cols=st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
