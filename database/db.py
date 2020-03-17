from firebase import firebase

import database.firebase_keys as keys

from database.db_users import DBAuth
from database.db_map import DBMap
from database.db_station import DBStation


class Database:
    def __init__(self):
        self.database = firebase.FirebaseApplication(keys.database_name,
                                                     authentication=None)

        self.db_users = DBAuth(self.database)
        self.db_map = DBMap(self.database)
        self.db_station = DBStation(self.database)


db = Database()
