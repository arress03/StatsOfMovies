from database import session, User, UserMovie

# Fonction pour ajouter ou se connecter à un utilisateur
def add_user(username):
    # Vérifie si l'utilisateur existe déjà
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print(f"Utilisateur '{username}' déjà existant. Connexion...")
        return existing_user
    else:
        # Si l'utilisateur n'existe pas, on le crée
        user = User(username=username)
        session.add(user)
        session.commit()
        print(f"Utilisateur '{username}' ajouté.")
        return user

# Fonction pour récupérer la watchlist de l'utilisateur
def get_watchlist(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        # Rechercher les films dans la watchlist
        watchlist = session.query(UserMovie).filter_by(user_id=user.id).all()
        return watchlist
    else:
        return []
