import csv

from movie_web_app.domain.model import Movie, Actor, Genre, Director

class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name

        self.__dataset_of_movies = list()
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()

        self.__subset_of_movie_directors = dict()


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

    @property
    def subset_of_movie_directors(self):
        return self.__subset_of_movie_directors

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
                #print("~~~~~")
                for actor in range(len(actors)):
                    actors[actor] = Actor(actors[actor].strip())
            #added
                    movie.actors.append(actors[actor].actor_full_name)
                    #print(actors[actor].actor_full_name)
            #end added
                    if actors[actor] not in self.dataset_of_actors:
                        self.dataset_of_actors.add(actors[actor])
                    #if row['Title'] == "Fury":
                        #print("de", actors[actor])
                #print(actors)

                director = Director(row['Director'])
                if director not in self.dataset_of_directors:
                    self.dataset_of_directors.add(director)
                #self.subset_of_movie_directors[str(title)] = []

                genres = row['Genre'].split(",")
                for genre in range(len(genres)):
                    genres[genre] = Genre(genres[genre].strip())
            # added
                    movie.genres.append(genres[genre].genre_name)
            # end added
                    if genres[genre] not in self.dataset_of_genres:
                        self.dataset_of_genres.add(genres[genre])
                        #self.dataset_of_genres.append( Genre(genres[genre]) )
                #print(genres)

            # added
                movie.director = row['Director']
                movie.description = row['Description']
                movie.runtime_minutes = int(row['Runtime (Minutes)'])
            # end added

                index += 1
