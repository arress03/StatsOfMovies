import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from tkinter import messagebox, Entry, Label, Button, Frame
from tkinter import Tk, StringVar
from user_functions import add_user, get_watchlist
from database import session

# Charger les variables d'environnement depuis .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'

# Fonction pour rechercher des films par nom
def search_movies(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print("Erreur lors de la recherche de films.")
        return []

# Création de l'interface graphique
class MovieApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de films")
        self.geometry("800x600")
        self.configure(bg="#2e2e2e")  # Fond gris foncé pour éviter l'effet blanc

        # Variables utilisateur
        self.username = StringVar()
        self.current_user = None  # Pour stocker l'utilisateur connecté
        self.watchlist = []  # Pour stocker la watchlist

        # Demande de l'utilisateur sur la même page principale
        self.setup_username_entry()

    def setup_username_entry(self):
        # Label et champ de texte pour le nom d'utilisateur
        Label(self, text="Entrez votre nom d'utilisateur :", bg="#2e2e2e", fg="white", font=("Arial", 16)).pack(pady=10)
        self.username_entry = Entry(self, textvariable=self.username, font=("Arial", 14))
        self.username_entry.pack(pady=10)
        self.confirm_button = Button(self, text="Confirmer", command=self.confirm_username, font=("Arial", 12), bg="#5a5a5a", fg="white")
        self.confirm_button.pack(pady=10)

    def confirm_username(self):
        username = self.username.get()
        if username:
            # Connexion ou ajout de l'utilisateur
            self.current_user = add_user(username)
            # Récupération de la watchlist
            self.watchlist = get_watchlist(username)
            print(f"Watchlist pour {username}:", [movie.movie_id for movie in self.watchlist])
            self.setup_main_menu()
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un nom d'utilisateur.")

    def setup_main_menu(self):
        # Effacer le champ d'utilisateur et bouton de confirmation
        self.username_entry.pack_forget()
        self.confirm_button.pack_forget()

        # Menu principal avec deux boutons
        Button(self, text="Partie Statistique", command=self.show_stat_page, width=30, height=2, bg="#5a5a5a", fg="white", font=("Arial", 12)).pack(pady=10)
        Button(self, text="Recommandations Personnalisées", command=self.show_recommend_page, width=30, height=2, bg="#5a5a5a", fg="white", font=("Arial", 12)).pack(pady=10)

    # Page Statistique
    def show_stat_page(self):
        for widget in self.winfo_children():
            widget.pack_forget()
        
        Label(self, text="Analyse des genres par année", font=("Arial", 16), bg="#2e2e2e", fg="white").pack(pady=10)
        self.year_entry = Entry(self, font=("Arial", 14))
        self.year_entry.pack(pady=10)
        Button(self, text="Lancer l'analyse", command=self.launch_genre_analysis, bg="#5a5a5a", fg="white").pack(pady=10)
        Button(self, text="Retour au menu principal", command=self.setup_main_menu, bg="#5a5a5a", fg="white").pack(pady=10)

    # Page Recommandation
    def show_recommend_page(self):
        for widget in self.winfo_children():
            widget.pack_forget()
        
        Label(self, text="Sélectionnez vos films préférés", font=("Arial", 16), bg="#2e2e2e", fg="white").pack(pady=10)
        self.movie_search_entry = Entry(self, font=("Arial", 14))
        self.movie_search_entry.pack(pady=10)
        Button(self, text="Rechercher", command=self.search_movies_interface, bg="#5a5a5a", fg="white").pack(pady=10)
        Button(self, text="Retour au menu principal", command=self.setup_main_menu, bg="#5a5a5a", fg="white").pack(pady=10)

    # Fonction pour lancer l'analyse des genres
    def launch_genre_analysis(self):
        try:
            year = int(self.year_entry.get())
            print(f"Analyzing genre trends for the year {year}")  # Placeholder
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer une année valide.")

    # Interface de recherche de films
    def search_movies_interface(self):
        query = self.movie_search_entry.get()
        results = search_movies(query)
        print(f"Recherche de films pour : {query}")  # Placeholder


# Lancer l'application
if __name__ == "__main__":
    app = MovieApp()
    app.mainloop()
