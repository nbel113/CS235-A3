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

