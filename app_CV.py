import streamlit as st
import pickle
import requests

# Chargement des données
movies = pickle.load(open('C:\\Users\\pauli\\Desktop\\FICHIERS VS CODE\\FILMS\\movies_list_CV.pkl', 'rb'))
similarity = pickle.load(open('C:\\Users\\pauli\\Desktop\\FICHIERS VS CODE\\FILMS\\similarity_CV.pkl', 'rb'))

# Configuration de la page en mode large
st.set_page_config(layout="wide", page_title="Movies Recommendation", page_icon="🎬")

# Variable valeurs titres des films pour la selectbox utilisateur
movies_list = movies['Titre'].values

st.header("Recommandation de films")  # Titre de l'application
selectvalue = st.selectbox("Choisissez un film dans le menu", movies_list)  # Sélection du film

# Fonction pour récupérer le poster d'un film à partir de son id
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=02764d983683e88872bd028c7f3f3f2e'
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
        return full_path
    return None

# Fonction pour récupérer l'overview d'un film à partir de son id en français
def fetch_overview(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=02764d983683e88872bd028c7f3f3f2e&language=fr'
    data = requests.get(url).json()
    overview = data.get('overview', 'Aucun overview disponible')
    return overview

# Fonction pour recommander les films similaires à un film donné
def recommend(movie):
    index = movies[movies['Titre'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].Titre)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

if selectvalue:
    if st.button("Voir les recommandations"):
        movie_names, movie_posters = recommend(selectvalue)
        col1, col2, col3, col4, col5 = st.columns(5)
        columns = [col1, col2, col3, col4, col5]

        for col, movie_name, movie_poster in zip(columns, movie_names, movie_posters):
            with col:
                if movie_poster:
                    st.image(movie_poster)
                if st.button(movie_name):
                    # Récupérer et afficher l'overview en français
                    movie_id = movies[movies['Titre'] == movie_name].iloc[0]['id']
                    overview = fetch_overview(movie_id)
                    st.write(f"Overview du film : {overview}")
    else:
        st.warning("Veuillez sélectionner un film dans le menu.")