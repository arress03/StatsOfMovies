import streamlit as st
from functions import search_movies, save_movie_to_csv, analyze_genres, get_available_genres, analyze_director_movies_by_year, analyze_director_ratings
import pandas as pd

# Interface utilisateur principale
st.title("StatsOfMovies By Théo TEPER")

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv("movies.csv")

data = load_data()

# Navigation
menu = ["Recherche de films", "Analyse des genres", "Analyse des réalisateurs"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Recherche de films":
    st.header("Recherche de films")
    query = st.text_input("Entrez un titre ou un genre de film")
    if query:
        st.write(f"Recherche en cours pour : {query}")
        results = search_movies(query)
        if results:
            for movie in results[:5]:  # Limiter à 5 résultats
                st.image(movie["poster_path"], width=150)
                st.write(f"**Titre :** {movie['title']}")
                st.write(f"**Date de sortie :** {movie['release_date']}")
                st.write(f"**Genres :** {', '.join(movie['genres'])}")
                st.write(f"**Réalisateur :** {movie['director']}")
                st.write(f"**Acteurs principaux :** {', '.join(movie['actors'])}")
                st.write(f"**Budget :** ${movie['budget']:,.2f}")
                st.write(f"**Recette :** ${movie['revenue']:,.2f}")

                if st.button(f"Enregistrer {movie['title']}", key=movie["id"]):
                    save_movie_to_csv(movie)
        else:
            st.error("Aucun résultat trouvé. Essayez un autre titre ou genre.")

elif choice == "Analyse des genres":
    st.header("Analyse des genres")

    start_year = st.number_input("Année de début", min_value=1900, max_value=2100, value=2000)
    end_year = st.number_input("Année de fin", min_value=1900, max_value=2100, value=2020)

    # Ajouter une liste déroulante pour les genres disponibles
    available_genres = get_available_genres()
    genre = st.selectbox("Choisissez un genre à analyser", options=available_genres)

    if st.button("Analyser"):
        analyze_genres(genre=genre, start_year=start_year, end_year=end_year)

elif choice == "Analyse des réalisateurs":
    st.header("Analyse des réalisateurs")
    option = st.radio("Options :", ["Nombre de films par année", "Distribution des notes"])
    director_name = st.text_input("Entrez le nom du réalisateur :", placeholder="Exemple : Christopher Nolan")

    if option == "Nombre de films par année" and director_name:
        movies_per_year = analyze_director_movies_by_year(director_name)
        if not movies_per_year.empty:
            st.bar_chart(movies_per_year)
        else:
            st.warning(f"Aucune donnée trouvée pour le réalisateur {director_name}.")

    elif option == "Distribution des notes" and director_name:
        avg_rating, ratings_distribution = analyze_director_ratings(director_name)
        if avg_rating > 0:
            st.write(f"Note moyenne : {avg_rating:.2f}")
            st.bar_chart(ratings_distribution)
        else:
            st.warning(f"Aucune donnée disponible pour les notes du réalisateur {director_name}.")
