
from streamlit import *
import streamlit as st 
import requests
import joblib
df=joblib.load('dfanime')
tfidf_matrix=joblib.load('animev')
from sklearn.metrics.pairwise import  cosine_similarity
hide_menu="""
<style>
#MainMenu{visibility:hidden;
}
img {
    width:500px;
    height: 500px;
}
</style>


"""
st.set_page_config(layout="wide")
def fetch_poster(movie_id):
    url = "https://api.jikan.moe/v4/anime/{}".format(movie_id)
    data = requests.get(url)
    data = data.json()
    try:
        poster_path = data["data"]["images"]["jpg"]["large_image_url"]

        full_path = str( poster_path)
        return full_path
    except Exception as e:
        return str("Something went/n Wrong")


def recommend(movie):
    index = df[df['English name'] == movie].index[0]
    sim_scores = list(enumerate(cosine_similarity(tfidf_matrix,tfidf_matrix[index])))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recommended_movie_names = []
    recommended_movie_posters=[]
    for i in sim_scores[1:11]:
        movie_id = df.iloc[i[0]].anime_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(df.iloc[i[0]]['English name'])

    return recommended_movie_names,recommended_movie_posters
menu_choice = st.sidebar.radio("Select an option", ("Home", "About"))

if menu_choice == "Home":
    
    st.markdown(hide_menu,unsafe_allow_html=True)
    st.title("Welcome to the Homepage")
    st.header('Anime Recommender')
    movie_list = df['English name'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )


    if st.button('Show Recommendation'):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            if recommended_movie_posters[0]=="Something went/n Wrong":
                st.error("!Oops Something went wrong")
            else:
                st.image(recommended_movie_posters[0],use_column_width='auto')
            
        with col2:
            st.text(recommended_movie_names[1])
            if recommended_movie_posters[1]=="Something went/n Wrong":
                st.error("!Oops Something went wrong")
            else:
                st.image(recommended_movie_posters[1],use_column_width='auto')
            
        with col3:
            st.text(recommended_movie_names[2])
            if recommended_movie_posters[2]=="Something went/n Wrong":
                st.error("!Oops Something went wrong")
            else:
                st.image(recommended_movie_posters[2],use_column_width='auto')
            
        with col4:
            st.text(recommended_movie_names[3])
            if recommended_movie_posters[3]=="Something went/n Wrong":
                st.error("!Oops Something went wrong")
            else:
                st.image(recommended_movie_posters[3],use_column_width='auto')
            
        with col5:
            st.text(recommended_movie_names[4])
            if recommended_movie_posters[4]=="Something went/n Wrong":
                st.error("!Oops Something went wrong")
            else:
                st.image(recommended_movie_posters[4],use_column_width='auto')
            
if menu_choice=="About":
    st.title("About Us")
    st.write("Learn more about our company and mission here.")
    st.write("This is my first streamlit project")
    st.write("It is an anime recommendation app that gives you five similar anime to the anime you choose.")

