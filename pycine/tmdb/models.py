from enum import Enum

class Genre(Enum):
    Drama = 18
    Comedia = 35
    Scifi = 878

class TMDBPeople:
    def __init__(self, 
            id, 
            name, 
            popularity=None,
            profile_path=None,
        ):
        self.id = id
        self.name = name
        self.popularity = popularity
        self.profile_path = profile_path

class TMDBMovie:
    def __init__(self, 
            id, 
            title, 
            popularity=None,
            poster_path=None,
            release_date=None,
            genres=None
        ):
        self.id = id
        self.title = title
        self.popularity = popularity
        self.poster_path = poster_path
        self.release_date = release_date
        self.genres = genres

