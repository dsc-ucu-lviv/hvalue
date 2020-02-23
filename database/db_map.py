class DBMap:
    def __init__(self, database):
        self.db = database
        # super(DBMap, self).__init__()

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
                            'receive_station_type': list(receive_station_id),
                            'time_from': str,
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
        response = self.db.get("receiver_stations", None)
        self.checking(rcv_station_dict, response)
        return response

    def checking(self, user_station, stations):
        """
        Return all suitable for a user stations,
        otherwise return []
        :param user_station: dict = {(str): int, (str): (str), ...}
        :param stations:  dict = {(str): list, (str): (int), (str): (str), ...}
        :return: list = [(dict), ...]
        """
        suitable_stations = []
        for station in stations:
            if self._data_intersection(user_station['categories'], station['categories']):
                if self._data_intersection(user_station['city_id'], station['locations']):
                    if self._data_intersection(user_station['receive_station_type'], station['type_id']):

                        s_dates = self._get_all_dates(station['time_from'], station['time_to'])
                        u_dates = self._get_all_dates(user_station['time_from'], user_station['time_to'])
                        if self._data_intersection(s_dates, u_dates):
                            suitable_stations.append(station)

        return suitable_stations

    @staticmethod
    def _data_intersection(user_data, database_data):
        """
        Return True if user_data has some elements in common
        with database_data
        :return: (bool)
        """
        if not isinstance(user_data, list):
            user_data = [user_data]
        if not isinstance(database_data, list):
            database_data = [database_data]

        user_set = set(user_data)
        database_set = set(database_data)

        if user_set.intersection(database_set) != set():
            return True
        else:
            return False

    @staticmethod
    def _get_all_dates(time_from, time_to):
        """
        Return list of all dates between time_from and time_to
        :param time_from: (str) eg. "2020-02-01"
        :param time_to: (str) eg. "2020-10-27"
        :return: list = [datetime.date(int, int, int), ...]
        """
        from datetime import date, timedelta
        s_time_from = time_from.split('-')
        s_time_to = time_to.split('-')

        s_time_from = list(map(lambda x: int(x), s_time_from))
        s_time_to = list(map(lambda x: int(x), s_time_to))

        start_date_s = date(s_time_from[0], s_time_from[1], s_time_from[2])  # start date
        end_date_s = date(s_time_to[0], s_time_to[1], s_time_to[2])  # end date

        delta = end_date_s - start_date_s  # as timedelta

        available_dates = []
        for i in range(delta.days + 1):
            day = start_date_s + timedelta(days=i)
            available_dates.append(day)

        return available_dates
