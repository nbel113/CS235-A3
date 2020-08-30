from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

class Movie:
    #A movie is considered to be uniquely defined by the combination of its title and release year, i.e. we assume that no two movies with the same title are released in the same year.
    def __init__(self, title: str, release_year: int):
        self.__description = ""
        self.__director = Director(None)
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes: int = 0

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

