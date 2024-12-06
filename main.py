import streamlit as st
from functions import (
    search_movies,
    save_movie_to_csv,
    analyze_genres,
    analyze_directors,
    analyze_actors,
    analyze_geography,
    analyze_budget_revenue,
    visualize_saved_movies,
)

# Configuration de l'interface
st.set_page_config(page_title="Film Data Analysis Dashboard", layout="wide")
st.title("Film Data Analysis Dashboard")

# Navigation principale
menu = st.sidebar.radio(
    "Navigation",
    [
        "Recherche de films",
        "Analyse des genres",
        "Analyse des réalisateurs",
        "Analyse des acteurs",
        "Analyse géographique",
        "Analyse des budgets et revenus",
        "Visualisation des films enregistrés",
    ],
)

# Recherche de films
if menu == "Recherche de films":
    st.header("Recherche de films")
    query = st.text_input("Entrez un titre ou un genre de film")
    if query:
        results = search_movies(query)
        if results:
            for movie in results[:5]:  # Limiter à 5 résultats
                st.image(movie["poster_path"], width=150)
                st.write(f"**Titre :** {movie['title']}")
                st.write(f"**Date de sortie :** {movie['release_date']}")
                st.write(f"**Genres :** {', '.join(movie['genres'])}")
                st.write(f"**Réalisateur :** {movie['director']}")
                st.write(f"**Acteurs principaux :** {', '.join(movie['actors'])}")

                if st.button(f"Enregistrer {movie['title']}", key=movie["id"]):
                    save_movie_to_csv(movie)
                    st.success(f"Film '{movie['title']}' enregistré avec succès.")
        else:
            st.error("Aucun résultat trouvé. Essayez un autre titre ou genre.")

# Analyse des genres
elif menu == "Analyse des genres":
    st.header("Analyse des genres")
    filter_type = st.selectbox("Filtrer par :", ["Année", "Genre"])
    if filter_type == "Année":
        year = st.number_input("Entrez une année", min_value=1900, max_value=2024, step=1)
        if st.button("Analyser"):
            analyze_genres(year=year)
    elif filter_type == "Genre":
        genre = st.text_input("Entrez un genre")
        if st.button("Analyser"):
            analyze_genres(genre=genre)

# Analyse des réalisateurs
elif menu == "Analyse des réalisateurs":
    st.header("Analyse des réalisateurs")
    director = st.text_input("Entrez le nom d'un réalisateur")
    if st.button("Analyser"):
        analyze_directors(director)

# Analyse des acteurs
elif menu == "Analyse des acteurs":
    st.header("Analyse des acteurs")
    actor = st.text_input("Entrez le nom d'un acteur")
    if st.button("Analyser"):
        analyze_actors(actor)

# Analyse géographique
elif menu == "Analyse géographique":
    st.header("Analyse géographique")
    filter_type = st.selectbox("Filtrer par :", ["Année", "Pays"])
    if filter_type == "Année":
        year = st.number_input("Entrez une année", min_value=1900, max_value=2024, step=1)
        if st.button("Analyser"):
            analyze_geography(year=year)
    elif filter_type == "Pays":
        country = st.text_input("Entrez un pays")
        if st.button("Analyser"):
            analyze_geography(country=country)

# Analyse des budgets et revenus
elif menu == "Analyse des budgets et revenus":
    st.header("Analyse des budgets et revenus")
    analyze_budget_revenue()

# Visualisation des films enregistrés
elif menu == "Visualisation des films enregistrés":
    st.header("Visualisation des films enregistrés")
    visualize_saved_movies()
