from database.db_base import DBBase


class DBMap(DBBase):
    def __init__(self, database):
        super().__init__(database)

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

    def get_organization_types(self):
        # TODO: implement
        return NotImplementedError

    def get_easy_rcv_station(self, rcv_station_dict):
        """
        Return all available receiver_station in database that match requirements.
        rcv_station_dict = {'city': Lviv,
                            'time_from': 01-01-2018,
                            'time_to': 01-12-2050,
                            'type_id': ['container', 'organisation'],
                            'organizations': ['orphanage', 'shelter', 'charitable', 'others'],
                            'categories': ['money', 'clothes', 'food']}
        :return: (dict) {receiver_station_type_id: {username: str,
                                                    type: ['container', 'organisation'],
                                                    categories: ['money', 'clothes', 'food'],
                                                    time_from: str,
                                                    time_to: str,
                                                    locations: [(lat, lon)],
                                                    description: str}
        """
        pass

    def get_receive_stations(self, rcv_station_dict):
        """
        Return all available receiver_station in database that match requirements.
        rcv_station_dict = {'city_id': int,
                            'time_from': str,
                            'time_to': str,
                            'type_id': list(int),
                            'organizations': list(user_id),
                            'categories': list(categories_id)}
        :return: (dict) {receiver_station_type_id: {user_id: int,
                                                    type_id: int,
                                                    categories: list(int),
                                                    time_from: str,
                                                    time_to: str,
                                                    locations: list(int),
                                                    description: str}
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

        if user_set and (user_set.intersection(database_set) == set()):
            return False
        if user_station['type_id'] and (station['type_id'] not in user_station['type_id']):
            return False
        if user_station['organisations'] and (self._get_organization_type(station['user_id'])
                                              not in user_station['organisations']):
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
        return self.db.get('locations/{}'.format(location_id), None)

    def _get_organization_type(self, user_id):
        return self.db.get('users/{}/type_id'.format(user_id), None)
