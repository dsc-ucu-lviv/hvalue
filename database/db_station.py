from database.db_base import DBBase

back_category_types = {0: 'money', 1: 'clothes', 2: 'food'}


class DBStation(DBBase):
    def __init__(self, database, parent):
        super().__init__(database)
        self.parent = parent

        self.t_new_rcv_stations = '/new_receive_stations'
        self.t_rcv_stations = '/receive_stations'

    def get_profile_info(self, user_id):
        """
        :param user_id:
        :return: (dict) {'username': str, 'phone_number': str / None, 'email': str,
        'stations': [{'name': str, 'address': str, 'categories': ['food' ... ]}]}
        """
        user_info = self.parent.db_users.get_general_user_info(user_id)
        if 'phone_number' not in user_info:
            user_info['phone_number'] = None
        user_info['stations'] = self.get_stations(user_id)
        # print(user_info['stations'])
        return user_info

    def get_stations(self, user_id):
        all_stations = self.db.get("receive_stations", None)
        # print(all_stations)
        return_stations = []
        for st in all_stations:
            print(st)
            if st and st['user_id'] == user_id:
                loc = self.parent.db_locations.get_location_info(0, st['locations'][0])
                return_stations.append({'name': st['name'], 'address': loc['address'],
                                        'categories': [back_category_types[type] for type in st['categories']]})
        return return_stations

    def add_easy_rcv_station(self, station_dict):
        """
        Add station directly to database.
        :param station_dict: = {'user_id': int,
                                'type_id': int,
                                'name': str,
                                'categories': list(int),
                                'address': str,
                                'time_from': str,
                                'time_to': str,
                                'description': str}
        :return: None / Error
        """
        loc_id = self.parent.db_locations.add_new_location({'city_id': 0, "address": station_dict['address']})
        new_station_dict = {'user_id': station_dict['user_id'],
                            'type_id': station_dict['type_id'],
                            'name': station_dict['name'],
                            'categories': station_dict['categories'],
                            'locations': {0: loc_id},
                            'time_from': station_dict['time_from'],
                            'time_to': station_dict['time_to'],
                            'description': station_dict['description']}
        self.increase_last_id('receive_station_id')
        self.db.put(self.t_rcv_stations, self.get_last_id('receive_station_id'), new_station_dict)

    def add_new_rcv_station(self, station_dict):
        """
        Send new station for review.
        :param station_dict: = {'user_id': int,
                                'type_id': int,
                                'categories': list(int),
                                'locations': list(location_id),
                                'time_from': str,
                                'time_to': str,
                                'description': str}
        :return: None / Error
        """
        if not {'user_id', 'type_id', 'categories', 'locations',
                'time_from', 'time_to', 'description'}.issubset(station_dict):
            raise KeyError

        if not (self.valid_date_format(station_dict['time_from'])
                and self.valid_date_format(station_dict['time_from'])):
            raise TypeError

        # TODO: check user existence and other ids
        # In case there other irrelevant keys in user_dict -> creating new dict
        new_station_dict = {'user_id': station_dict['user_id'],
                            'type_id': station_dict['type_id'],
                            'categories': station_dict['categories'],
                            'locations': station_dict['locations'],
                            'time_from': station_dict['time_from'],
                            'time_to': station_dict['time_to'],
                            'description': station_dict['description'],
                            'status': ""}

        self.increase_last_id('new_receive_stations_id')
        self.db.put(self.t_new_rcv_stations, self.get_last_id('new_receive_stations_id'), new_station_dict)
