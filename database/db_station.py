from database.db_base import DBBase


class DBStation(DBBase):
    def __init__(self, database):
        super().__init__(database)

        self.t_new_rcv_stations = '/new_receive_stations'

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
