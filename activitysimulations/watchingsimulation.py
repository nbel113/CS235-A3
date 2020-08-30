from domainmodel.movie import Movie
from domainmodel.user import User
from domainmodel.review import Review

class MovieWatchingSimulation:
    def __init__(self):
        self.__movies = list()
        self.__movie_dict = dict()
    def add_movie_review(self, movie, user, review_rating):
        if movie not in self.__movies:
            self.__movies.append(movie)
            self.__movie_dict[movie] = []
        self.__movie_dict[movie].append([user, review_rating])
    def get_movie_rating_average(self, movie):
        if movie not in self.__movies:
            return ("Unrated: No Reviews")
        average = 0
        count = 0
        for i in self.__movie_dict[movie]:
            average += i[1]
            count += 1
        average = round(average/count, 2)
        return f"Average Rating: {average}"
    @property
    def movie_dict(self):
        return self.__movie_dict