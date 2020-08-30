import csv

from domainmodel.movie import Movie
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.director import Director

class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name

        self.__dataset_of_movies = list()
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies
    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors
    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors
    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                #print(f"Movie {index} with title: {title}, release year {release_year}")
                movie = Movie(title, release_year)
                if movie not in self.dataset_of_movies:
                    self.dataset_of_movies.append(movie)

                actors = row['Actors'].split(",")
                for actor in range(len(actors)):
                    actors[actor] = Actor(actors[actor].strip())
                    if actors[actor] not in self.dataset_of_actors:
                        self.dataset_of_actors.add(actors[actor])
                    #if row['Title'] == "Fury":
                        #print("de", actors[actor])
                #print(actors)

                director = Director(row['Director'])
                if director not in self.dataset_of_directors:
                    self.dataset_of_directors.add(director)
                #print(director)

                genres = row['Genre'].split(",")
                for genre in range(len(genres)):
                    genres[genre] = Genre(genres[genre].strip())
                    if genres[genre] not in self.dataset_of_genres:
                        self.dataset_of_genres.add(genres[genre])
                        #self.dataset_of_genres.append( Genre(genres[genre]) )
                #print(genres)

                index += 1