from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

# Initialisation de la base de données SQLite
engine = create_engine('sqlite:///movies_app.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Définition des tables
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    
    movies = relationship("UserMovie", back_populates="user")

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    popularity = Column(Float)
    
    users = relationship("UserMovie", back_populates="movie")

class UserMovie(Base):
    __tablename__ = 'user_movies'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    rating = Column(Float)  # Note personnelle de l'utilisateur
    watched_date = Column(Date, default=date.today)

    user = relationship("User", back_populates="movies")
    movie = relationship("Movie", back_populates="users")

# Créer les tables dans la base de données
Base.metadata.create_all(engine)
