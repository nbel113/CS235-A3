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
            self.__time_spent_watching_movies_minutes = None
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