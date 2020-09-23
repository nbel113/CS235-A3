import csv
from werkzeug.security import generate_password_hash
from movie_web_app.domain.model import User

class UserFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name = file_name

        self.__dataset_of_users = list()

    @property
    def dataset_of_users(self):
        return self.__dataset_of_users

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            user_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in user_file_reader:
                user_name = row['user_name']
                password = generate_password_hash(row['password'])
                user = User(user_name, password)
                if user not in self.dataset_of_users:
                    self.dataset_of_users.append(user)
                index += 1