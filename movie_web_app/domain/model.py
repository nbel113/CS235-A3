from datetime import datetime
import uuid #universially unique identifiers

class Director:
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        return self.__director_full_name == other.__director_full_name

    def __lt__(self, other):
        if not isinstance(self, Director) or not isinstance(other, Director):
            return False
        if self.__director_full_name < other.__director_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.__director_full_name)
		
class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        return self.__genre_name == other.__genre_name

    def __lt__(self, other):
        if not isinstance(self, Genre) or not isinstance(other, Genre):
            return False
        if self.__genre_name < other.__genre_name:
            return True
        return False

    def __hash__(self):
        return hash(self.__genre_name)
		
class Actor:
    def __init__(self, actor_full_name: str):
        self.__actor_colleague_list = []
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        if not isinstance(self, Actor) or not isinstance(other, Actor):
            return False
        if self.__actor_full_name < other.__actor_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.__actor_full_name)

    # if an actor colleague was on the cast for the same movie as this actor, we allow for the colleague to be added to this actor's set of colleagues
    def add_actor_colleague(self, colleague):
        self.__actor_colleague_list.append(colleague)

    # this method checks if a given colleague Actor has worked with the actor at least once in the same movie
    def check_if_this_actor_worked_with(self, colleague):
        return (colleague in self.__actor_colleague_list)

class Movie:
    #A movie is considered to be uniquely defined by the combination of its title and release year, i.e. we assume that no two movies with the same title are released in the same year.
    def __init__(self, title: str, release_year: int):
        self.__description = ""
        self.__director = Director(None)
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes: int = 0
        #self.__metascore = 0

        if (title == "") or (type(title) is not str) or (release_year < 1900) or (type(release_year) is not int):
            self.__title = None
            self.__release_year = None
        else:
            self.__title = title.strip()
            self.__release_year = release_year

    @property
    def title(self) -> str:
        return self.__title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self) -> str:
        return self.__description
    @description.setter
    def description(self, description: str):
        self.__description = description.strip()

    @property
    def director(self):
        return self.__director
    @director.setter
    def director(self, director):
        self.__director = director

    @property
    def actors(self):
        return self.__actors
    def add_actor(self, actor):
        self.__actors.append(actor)
    def remove_actor(self, actor):
        if (actor in self.__actors):
            self.__actors.remove(actor)

    @property
    def genres(self):
        return self.__genres
    def add_genre(self, genre):
        self.__genres.append(genre)
    def remove_genre(self, genre):
        if (genre in self.__genres):
            self.__genres.remove(genre)

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes
    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes: int):
        if runtime_minutes < 0:
            raise ValueError
        self.__runtime_minutes = runtime_minutes

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if (self.__title == other.__title) and (self.__release_year == other.__release_year):
            return True
        return False

    #movie name, then release date
    def __lt__(self, other):
        if not isinstance(self, Movie) or not isinstance(other, Movie):
            return False
        if self.__title < other.__title:
            return True
        if self.__title == other.__title and self.__release_year < other.__release_year:
            return True
        return False

    def __hash__(self):
        unique_string = self.__title + str(self.__release_year)
        return hash(unique_string)

class Review:
    #added review_id to model, since my program allows users to make reviews with the same movie title, review text and score
    def __init__(self, movie, review_text, rating):
        self.__review_id = None
        self.__movie = None #Movie(None, None)
        self.__review_text = None
        self.__rating = None
        self.__timestamp = None #datetime.now()
        self.__latest_edit = None

        if (type(movie) is not Movie) \
                or (type(review_text) is not str) \
                or (type(rating) is not int) \
                or (rating < 1 or rating > 10):
            self.__review_id = None
            self.__movie = None
            self.__review_text = None
            self.__rating = None
            self.__timestamp = None
            self.__latest_edit = None
        else:
            self.__review_id = uuid.uuid1()
            self.__movie = movie
            self.__review_text = review_text.strip()
            self.__rating = rating
            self.__timestamp = datetime.now()
            self.__latest_edit = datetime.now()

    #added setters for the properties - review_id doesn't need to change

    @property
    def review_id(self):
        return self.__review_id

    @property
    def movie(self) -> Movie:
        return self.__movie
    @movie.setter
    def movie(self, new_movie) -> str:
        self.__movie = new_movie
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text
    @review_text.setter
    def review_text(self, new_review_text) -> str:
        self.__review_text = new_review_text
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating
    @rating.setter
    def rating(self, new_rating) -> int:
        self.__rating = new_rating
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    @timestamp.setter
    def timestamp(self, new_timestamp) -> datetime:
        self.__new_timestamp = new_timestamp
        return self.__timestamp

    @property
    def latest_edit(self) -> datetime:
        return self.__latest_edit
    @latest_edit.setter
    def latest_edit(self, new_latest_edit) -> datetime:
        self.__latest_edit = new_latest_edit
        return self.__latest_edit

    def __repr__(self):
        return f"<Review {self.__movie}, {self.__review_text}, {self.__rating}>"

    def __eq__(self, other):
        if (self.__movie == other.__movie) \
                and (self.__review_text == other.__review_text) \
                and (self.__rating == other.__rating) \
                and (self.__timestamp == other.__timestamp):
            return True
        return False

#TempReview is a copy of Review, It is designed to store input from the edit review form.
#If input for a property (eg review_text) is valid and not None/blank text (eg "" or " "), the original review will have that property updated with the input.
class TempReview:
    def __init__(self, movie: Movie, review_text, rating):
        self.__movie = movie
        self.__review_text = review_text
        self.__rating = rating
        self.__timestamp = datetime.now()

    @property
    def movie(self) -> Movie:
        return self.__movie
    @movie.setter
    def movie(self, new_movie) -> str:
        self.__movie = new_movie
        return self.__movie
    @property
    def review_text(self) -> str:
        return self.__review_text
    @review_text.setter
    def review_text(self, new_review_text) -> str:
        self.__review_text = new_review_text
        return self.__review_text
    @property
    def rating(self) -> int:
        return self.__rating
    @rating.setter
    def rating(self, new_rating) -> int:
        self.__rating = new_rating
        return self.__rating
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    @timestamp.setter
    def timestamp(self, new_timestamp) -> datetime:
        self.__new_timestamp = new_timestamp
        return self.__timestamp

    def __repr__(self):
        return f"<TempReview {self.__movie}, {self.__review_text}, {self.__rating}>"

    def __eq__(self, other):
        if (self.__movie == other.__movie) \
                and (self.__review_text == other.__review_text) \
                and (self.__rating == other.__rating) \
                and (self.__timestamp == other.__timestamp):
            return True
        return False

class User:
    def __init__(self, user_name, password):
        self.__user_name = None
        self.__password = None
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

        if (type(user_name) is not str) \
                or (type(password) is not str) \
                or (self.__time_spent_watching_movies_minutes < 0):
            self.__user_name = None
            self.__password = None
            self.__watched_movies = None
            self.__reviews = None
            self.__time_spent_watching_movies_minutes = 0
        else:
            self.__user_name = user_name.strip().lower()
            self.__password = password

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        if (self.__user_name == other.__user_name):
            return True
        return False

    def __lt__(self, other):
        if (self.__user_name < other.__user_name):
            return True
        return False

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie):
        if (movie not in self.__watched_movies):
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if (review not in self.__reviews):
            self.__reviews.append(review)

class WatchList:
    def __init__(self):
        self.__watchlist = list()

    def add_movie(self, movie):
        if movie not in self.__watchlist:
            self.__watchlist.append(movie)

    def remove_movie(self, movie):
        if movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def select_movie_to_watch(self, index):
        if index not in range(len(self.__watchlist)):
            return None
        return self.__watchlist[index]

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        if self.__watchlist == []:
            return None
        return self.__watchlist[0]

    def __iter__(self):
        self.movie_index = 0
        return self

    def __next__(self):
        try:
            result = self.__watchlist[self.movie_index]
        except IndexError:
            raise StopIteration()
        self.movie_index += 1
        return result