import requests
import pandas as pd
import streamlit as st

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
