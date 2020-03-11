from firebase import firebase

import database.firebase_keys as keys

from database.db_auth import DBAuth
from database.db_map import DBMap
from database.db_station import DBStation
from database.db_locations import DBLocations


class Database:
    def __init__(self):
        self.database = firebase.FirebaseApplication(keys.database_name,
                                                     authentication=None)

        self.db_auth = DBAuth(self.database)
        self.db_map = DBMap(self.database)
        self.db_station = DBStation(self.database)
        self.db_locations = DBLocations(self.database)


db = Database()
