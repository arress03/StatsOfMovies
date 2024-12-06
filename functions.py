import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from tmdbv3api import TMDb, Movie

# Configuration de l'API TMDb
tmdb = TMDb()
tmdb.api_key = "4a151fdfe38db01056b9f6f0189378ab"
tmdb.language = "fr"

movie_api = Movie()

# Recherche de films
def search_movies(query):
    results = movie_api.search(query)
    genres_mapping = {genre['id']: genre['name'] for genre in movie_api.genres()["genres"]}
    movies = []
    for result in results:
        movie = {
            "title": result.title,
            "release_date": result.release_date or "Date inconnue",
            "genres": [genres_mapping.get(genre_id, "Inconnu") for genre_id in result.genre_ids],
            "poster_path": f"https://image.tmdb.org/t/p/w500{result.poster_path}" if result.poster_path else None,
            "director": "Inconnu",  # Réalisation non incluse directement
            "actors": [],  # Acteurs principaux non inclus directement
            "id": result.id,
            "budget": 0,  # Budget par défaut
            "revenue": 0,  # Revenus par défaut
        }
        movies.append(movie)
    return movies

# Enregistrer un film dans le CSV
def save_movie_to_csv(movie, filename="data/movies.csv"):
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        data = pd.DataFrame(columns=["title", "release_date", "genres", "director", "actors", "budget", "revenue"])
    data = pd.concat([data, pd.DataFrame([movie])], ignore_index=True)
    data.to_csv(filename, index=False)

# Visualisation des films enregistrés
def visualize_saved_movies(filename="data/movies.csv"):
    try:
        data = pd.read_csv(filename)
        st.dataframe(data)
    except FileNotFoundError:
        st.warning("Aucun film enregistré. Enregistrez des films pour commencer.")

# Analyse des genres
def analyze_genres(year=None, genre=None, filename="data/movies.csv"):
    try:
        data = pd.read_csv(filename)
        if year:
            filtered = data[data["release_date"].str.startswith(str(year))]
            genre_counts = filtered["genres"].str.split(", ").explode().value_counts()
            st.bar_chart(genre_counts)
        elif genre:
            filtered = data[data["genres"].str.contains(genre, case=False, na=False)]
            yearly_counts = filtered.groupby(filtered["release_date"].str[:4]).size()
            st.line_chart(yearly_counts)
    except FileNotFoundError:
        st.error("Aucune donnée disponible pour l'analyse.")

# Analyse des réalisateurs
def analyze_directors(director, filename="data/movies.csv"):
    try:
        data = pd.read_csv(filename)
        filtered = data[data["director"].str.contains(director, case=False, na=False)]
        yearly_counts = filtered.groupby(filtered["release_date"].str[:4]).size()
        st.line_chart(yearly_counts)
    except FileNotFoundError:
        st.error("Aucune donnée disponible pour l'analyse.")

# Analyse des acteurs
def analyze_actors(actor, filename="data/movies.csv"):
    try:
        data = pd.read_csv(filename)
        filtered = data[data["actors"].str.contains(actor, case=False, na=False)]
        yearly_counts = filtered.groupby(filtered["release_date"].str[:4]).size()
        st.line_chart(yearly_counts)
    except FileNotFoundError:
        st.error("Aucune donnée disponible pour l'analyse.")

# Analyse géographique
def analyze_geography(year=None, country=None, filename="data/movies.csv"):
    try:
        data = pd.read_csv(filename)
        if year:
            filtered = data[data["release_date"].str.startswith(str(year))]
        elif country:
            filtered = data[data["genres"].str.contains(country, case=False, na=False)]
        st.map(filtered[["latitude", "longitude"]])
    except FileNotFoundError:
        st.error("Aucune donnée disponible pour l'analyse.")

# Analyse des budgets et revenus
def analyze_budget_revenue(filename="data/movies.csv"):
    try:
        data = pd.read_csv(filename)
        if "budget" in data.columns and "revenue" in data.columns:
            st.bar_chart(data[["budget", "revenue"]])
        else:
            st.warning("Aucune donnée de budget ou revenu disponible.")
    except FileNotFoundError:
        st.error("Aucune donnée disponible.")
