from database.db_base import DBBase


class DBMap(DBBase):
    def __init__(self, database):
        super().__init__(database)

    def get_cities(self):
        """
        Return all available cities in database.
        :return: (dict) {city_id: "city_name", ...}
        """
        return self.db.get('cities', None)

    def get_categories(self):
        """
        Return all available categories in database.
        :return: (dict) {category_id: "category_name", ...}
        """
        return self.db.get('categories', None)

    def get_receiver_station_types(self):
        """
        Return all available receiver_station_types in database.
        :return: (dict) {receiver_station_type_id: "receiver_station_type_name", ...}
        """
        return self.db.get('receive_station_types', None)

    def get_receive_stations(self, rcv_station_dict):
        """
        Return all available receiver_station in database that match requirements.
        rcv_station_dict = {'city_id': int,
                            'time_from': str,
                            'type_id': list(int),
                            'time_to': str,
                            'categories': list(categories_id)}
        :return: (dict) {receiver_station_type_id: {user_id: int,
                                                    type_id: int,
                                                    locations: list(int),
                                                    time_from: str,
                                                    time_to: str,
                                                    description: str,
                                                    categories: list(int),
                                                    items: list(int)}, ...}
        """
        response = self.db.get("receive_stations", None)
        return list(filter(lambda x: self.checking(rcv_station_dict, x), response))

    def checking(self, user_station, station):
        """
        Return all suitable for a user stations,
        otherwise return []
        :param user_station: dict = {(str): int, (str): (str), ...}
        :param station:  dict = {(str): list, (str): (int), (str): (str), ...}
        :return: list = [(dict), ...]
        """
        user_set = set(user_station['categories'])
        database_set = set(station['categories'])

        if user_set.intersection(database_set) == set():
            return False
        if station['type_id'] not in user_station['type_id']:
            return False
        if self.compare_dates(user_station['time_from'], station['time_to']) == 1:
            return False
        if self.compare_dates(user_station['time_to'], station['time_from']) == -1:
            return False

        for location in station['locations']:
            if user_station['city_id'] == self._get_location(location)['city_id']:
                return True
        return False

    def _get_location(self, location_id):
        """
        Return info about location
        :param location_id: int
        :return: dict
        """
        return self.db.get('location/{}'.format(location_id), None)
