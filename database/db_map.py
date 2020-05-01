from database.db_base import DBBase


cities = {'Lviv': 0}
rcv_station_types = {'container': 0, 'organisation': 1}
organisation_types = {'orphanage': 0, 'shelter': 1, 'charitable': 2, 'others': 3}
category_types = {'money': 0, 'clothes': 1, 'food': 2}

back_rcv_stations = {0: 'Container', 1: 'Organisation'}
back_org_types = {0: 'orphanage', 1: 'shelter', 2: 'charitable', 3: 'others'}
back_category_types = {0: 'money', 1: 'clothes', 2: 'food'}


class DBMap(DBBase):
    def __init__(self, database, parent):
        super().__init__(database)
        self.parent = parent

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
                            'station_type': ['container', 'organisation'],
                            'organisations': ['orphanage', 'shelter', 'charitable', 'others'],
                            'categories': ['money', 'clothes', 'food']}
        :return: (list) [{username: str,
                         type: ['container', 'organisation'],
                         categories: ['money', 'clothes', 'food'],
                         time_from: str,
                         time_to: str,
                         locations: [(lat, lon)],
                         description: str}
        """
        rcv_dict = {'city_id': cities[rcv_station_dict['city']],
                    'time_from': rcv_station_dict['time_from'],
                    'time_to': rcv_station_dict['time_to'],
                    'type_id': [rcv_station_types[type] for type in rcv_station_dict['station_type']],
                    'organisations': [organisation_types[type] for type in rcv_station_dict['organizations']],
                    'categories': [category_types[type] for type in rcv_station_dict['categories']]}
        response = self.get_receive_stations(rcv_dict)
        print(response)

        new_response_lst = []
        for station in response:
            if station is not None:
                new_station = dict()
                new_station['organization_name'] = self.parent.db_users.get_general_user_info(station['user_id'])['username']
                for loc in station['locations']:
                    loc_info = self.parent.db_locations.get_location_info(cities[rcv_station_dict['city']], loc)
                    new_station['lat'] = loc_info['latitude']
                    new_station['lng'] = loc_info['longitude']
                    new_station['needs'] = ', '.join([back_category_types[category_id] for category_id
                                                      in station['categories']])
                    new_station['url'] = '#'
                new_response_lst.append(new_station)

        return new_response_lst

    def get_receive_stations(self, rcv_station_dict):
        """
        Return all available receiver_station in database that match requirements.
        rcv_station_dict = {'city_id': int,
                            'time_from': str,
                            'time_to': str,
                            'type_id': list(int),
                            'organisations': list(user_id),
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
        print('real_response', response)
        return list(filter(lambda x: self.checking(rcv_station_dict, x), response))

    def checking(self, user_station, station):
        """
        Return all suitable for a user stations,
        otherwise return []
        :param user_station: dict = {(str): int, (str): (str), ...}
        :param station:  dict = {(str): list, (str): (int), (str): (str), ...}
        :return: list = [(dict), ...]
        """
        if station is None:
            return False

        user_set = set(user_station['categories'])
        database_set = set(station['categories'])

        if user_set and (user_set.intersection(database_set) == set()):
            print('user_set: {}', user_set, 'database_set: {}', database_set)
            print('bad categories')
            return False
        if user_station['type_id'] and (station['type_id'] not in user_station['type_id']):
            print('bad rcv type id')
            return False
        if user_station['organisations'] and (self._get_organization_type(station['user_id'])
                                              not in user_station['organisations']):
            print('organizations')
            return False
        if self.compare_dates(user_station['time_from'], station['time_to']) == 1:
            print('bad start date')
            return False
        if self.compare_dates(user_station['time_to'], station['time_from']) == -1:
            print('bad finish date')
            return False
        return True

    def _get_organization_type(self, user_id):
        return self.db.get('users/{}/type_id'.format(user_id), None)
