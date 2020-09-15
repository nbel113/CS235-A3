from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader


def main():
    filename = 'movie_web_app/a_adapters/data/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()



if __name__ == "__main__":
    main()