import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

API_KEY = "4a151fdfe38db01056b9f6f0189378ab"
BASE_URL = "https://api.themoviedb.org/3"

def search_movies(query):
    try:
        url = f"{BASE_URL}/search/movie"
        params = {"api_key": API_KEY, "query": query}
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()["results"]

        # Ajouter les genres, acteurs et réalisateurs si disponibles
        enriched_results = []
        for result in results:
            movie_id = result["id"]

            # Récupérer les détails supplémentaires du film
            details = get_movie_details(movie_id)
            if details:
                enriched_results.append(details)

        return enriched_results
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la recherche de films : {e}")
        return []
    except KeyError as e:
        st.error(f"Erreur de données API : {e}")
        return []

def get_movie_details(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {"api_key": API_KEY, "append_to_response": "credits"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        movie = response.json()

        # Récupérer les acteurs et réalisateurs
        director = "Inconnu"
        actors = []
        if "credits" in movie:
            crew = movie["credits"]["crew"]
            cast = movie["credits"]["cast"]
            director_info = next((member for member in crew if member["job"] == "Director"), None)
            if director_info:
                director = director_info["name"]
            actors = [actor["name"] for actor in cast[:5]]  # Limité aux 5 premiers acteurs

        return {
            "title": movie.get("title", "Inconnu"),
            "release_date": movie.get("release_date", "Inconnu"),
            "genres": [genre["name"] for genre in movie.get("genres", [])],
            "director": director,
            "actors": actors,
            "id": movie_id,
            "budget": movie.get("budget", 0),
            "revenue": movie.get("revenue", 0),
            "poster_path": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des détails du film : {e}")
        return None
    except KeyError as e:
        st.error(f"Erreur de données API : {e}")
        return None

def save_movie_to_csv(movie, csv_path="movies.csv"):
    try:
        # Charger ou créer le DataFrame
        try:
            existing_data = pd.read_csv(csv_path)
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=["title", "release_date", "genres", "director", "actors", "id", "budget", "revenue", "poster_path"])

        # Ajouter le film s'il n'existe pas déjà
        if movie["id"] not in existing_data["id"].values:
            new_row = pd.DataFrame([movie])
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)
            updated_data.to_csv(csv_path, index=False)
            st.success(f"Film '{movie['title']}' enregistré avec succès.")
        else:
            st.warning(f"Le film '{movie['title']}' est déjà enregistré.")
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement du film : {e}")

def get_available_genres():
    """
    Récupère tous les genres disponibles depuis TMDB.
    """
    try:
        url = f"{BASE_URL}/genre/movie/list"
        params = {"api_key": API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        genres = response.json()["genres"]
        return [genre["name"] for genre in genres]
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des genres : {e}")
        return []

def get_genre_id(genre_name):
    """
    Récupère l'ID d'un genre donné en fonction de son nom depuis TMDB.
    """
    try:
        url = f"{BASE_URL}/genre/movie/list"
        params = {"api_key": API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        genres = response.json()["genres"]
        for genre in genres:
            if genre["name"].lower() == genre_name.lower():
                return genre["id"]
        return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération des genres : {e}")
        return None

def analyze_genres(genre, start_year, end_year):
    """
    Analyse des genres en se basant sur les 50 meilleurs films les plus populaires pour chaque année.
    """
    try:
        genre_id = get_genre_id(genre)
        if not genre_id:
            st.error("Genre introuvable. Veuillez vérifier le nom du genre.")
            return

        movies_per_year = {}
        for year in range(start_year, end_year + 1):
            url = f"{BASE_URL}/discover/movie"
            params = {
                "api_key": API_KEY,
                "sort_by": "popularity.desc",
                "primary_release_year": year,
                "page": 1,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])

            for page in range(2, 3):
                params["page"] = page
                response = requests.get(url, params=params)
                response.raise_for_status()
                results.extend(response.json().get("results", []))

            genre_count = 0
            for movie in results:
                if genre_id in movie.get("genre_ids", []):
                    genre_count += 1

            movies_per_year[year] = genre_count

        years = list(movies_per_year.keys())
        counts = list(movies_per_year.values())

        plt.figure(figsize=(10, 6))
        plt.bar(years, counts, color="skyblue")
        plt.title(f"Nombre de films pour le genre '{genre}' entre {start_year} et {end_year}")
        plt.xlabel("Année")
        plt.ylabel("Nombre de films")
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Erreur lors de l'analyse des genres : {e}")

def get_director_movies(director_name):
    """
    Récupère les films d'un réalisateur donné en utilisant l'API TMDb.
    """
    url = f"{BASE_URL}/search/person"
    params = {"api_key": API_KEY, "query": director_name}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            person_id = results[0]["id"]
            return fetch_movies_by_director(person_id)
        else:
            return []
    else:
        st.error("Erreur lors de la connexion à l'API.")
        return []


def fetch_movies_by_director(director_id):
    """
    Récupère tous les films d'un réalisateur donné à partir de son ID.
    """
    url = f"{BASE_URL}/person/{director_id}/movie_credits"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        crew = response.json().get("crew", [])
        directed_movies = [movie for movie in crew if movie.get("job") == "Director"]
        return directed_movies
    else:
        return []


def analyze_director_movies_by_year(director_name):
    """
    Analyse le nombre de films par année d'un réalisateur.
    """
    movies = get_director_movies(director_name)
    if not movies:
        return {}

    years = []
    for movie in movies:
        release_date = movie.get("release_date", None)
        if release_date:
            year = release_date.split("-")[0]
            years.append(year)

    movies_per_year = pd.Series(years).value_counts().sort_index()
    return movies_per_year


def analyze_director_ratings(director_name):
    """
    Analyse la distribution des notes des films d'un réalisateur.
    """
    movies = get_director_movies(director_name)
    if not movies:
        return 0, pd.Series(dtype=int)

    ratings = [movie.get("vote_average", 0) for movie in movies if movie.get("vote_average") is not None]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    bins = [0, 2, 4, 6, 8, 10]
    labels = ["0-2", "2-4", "4-6", "6-8", "8-10"]
    ratings_distribution = pd.cut(ratings, bins=bins, labels=labels, include_lowest=True).value_counts().sort_index()

    return avg_rating, ratings_distribution