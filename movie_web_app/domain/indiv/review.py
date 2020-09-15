from datetime import datetime

from movie_web_app.domain.movie import Movie

class Review:
    def __init__(self, movie, review_text, rating):
        self.__movie = None #Movie(None, None)
        self.__review_text = None
        self.__rating = None
        self.__timestamp = None #datetime.now()

        if (type(movie) is not Movie) \
                or (type(review_text) is not str) \
                or (type(rating) is not int) \
                or (rating < 1 or rating > 10):
            self.__movie = None
            self.__review_text = None
            self.__rating = None
            self.__timestamp = None
        else:
            self.__movie = movie
            self.__review_text = review_text.strip()
            self.__rating = rating
            self.__timestamp = datetime.now()

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __repr__(self):
        return f"<Review {self.__movie}, {self.__review_text}, {self.__rating}>"

    def __eq__(self, other):
        if (self.__movie == other.__movie) \
                and (self.__review_text == other.__review_text) \
                and (self.__rating == other.__rating) \
                and (self.__timestamp == other.__timestamp):
            return True
        return False
