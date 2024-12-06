import streamlit as st
from functions import search_movies, save_movie_to_csv, analyze_genres, get_available_genres

# Interface utilisateur principale
st.title("Film Data Analysis Dashboard")

# Navigation
menu = ["Recherche de films", "Analyse des genres"]
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
