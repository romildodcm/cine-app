import requests
from tmdb.models import TMDBMovie, Genre, TMDBPeople
import json
from service import Service

# Professor
# key = 'd1da20fbfa65312b857fb7b517bf855c'

# Romildo
key = 'd8e583d92736044775dc494378d7697e'


class RequestApi:
    """
    
    Esta classe faz request para a API do tmdb,
    de acordo com funções pre-definidas do nosso app

    """
    @staticmethod
    def test():
        print('[ok] from RequestApi')

    @staticmethod
    def get_movie_popular_by_genre(genre: int):
        endpoint = f'https://api.themoviedb.org/3/discover/movie/?api_key={key}&certification_country=US&certification=R&sort_by=vote_count.desc&with_genres={genre}'
        r = requests.get(endpoint)
        # print(r.status_code) # deve retornar 200
        data = r.json()
        results = data['results']
        return results


    # nome do artista: "Arnold Schwarzenegger"
    # def get_artista_by_name(name)
    #     endpoint: search_person

    @staticmethod
    def get_artista(person_id):
        endpoint = f'https://api.themoviedb.org/3/person/{person_id}?api_key={key}'
        r = requests.get(endpoint)
        data = r.json()
        results = data
        return results

    @staticmethod
    def get_artista_by_name(name):
        endpoint = f'https://api.themoviedb.org/3/search/person?api_key={key}&query={name}'
        r = requests.get(endpoint)
        data = r.json()
        results = data['results']
        if len(results) == 0:
            return {}

        person_id = results[0]['id']
        result = RequestApi.get_artista(person_id)

        p = TMDBPeople(
            result['id'],
            result['name'],
            result['popularity'],
            result['profile_path'],
        )

        # print(f'person_id: {person_id}')
        # print(f'result: {result}')
        # print(f'p: {p}')

        return p

class MovieUtils:
    """
    classe utilitaria para ser usada no fastapi
    """
    @staticmethod
    def get_genres(genre_ids):
        genres = Service.get_genres()
        genres_names = [g['name'] for g in genres if g['id'] in genre_ids]
        return " | ".join(genres_names)

    @staticmethod
    def get_image_path(poster_path):
        return f"https://image.tmdb.org/t/p/w185{poster_path}"

    @staticmethod
    def get_movies(genre: int):
        # obter o titulo (original_title)
        # percorremos a lista de filmes (results)
        results = RequestApi.get_movie_popular_by_genre(genre)
        movies = []  # lista que armazena os filmes
        for movie in results:
            m = TMDBMovie(
                movie['id'],
                movie['original_title'],
                genres=MovieUtils.get_genres(
                    movie['genre_ids']
                ),
                poster_path=MovieUtils.get_image_path(
                    movie['poster_path']
                )
            )
            movies.append(m)
            # title = movie['original_title']
            # print(m.title, m.id)
        # print(f'Filmes encontrados: {len(results)}')        
        return movies