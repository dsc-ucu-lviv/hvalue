class DBMap:
    def __init__(self, database):
        self.db = database

        # TODO: Add link to some tables

    def get_cities(self):
        """
        Return all available cities in database.
        :return: (dict) {city_id: "city_name", ...}
        """
        raise NotImplementedError

    def get_categories(self):
        """
        Return all available categories in database.
        :return: (dict) {category_id: "category_name", ...}
        """
        raise NotImplementedError

    def get_receiver_station_types(self):
        """
        Return all available receiver_station_types in database.
        :return: (dict) {receiver_station_type_id: "receiver_station_type_name", ...}
        """
        raise NotImplementedError

    def get_receive_stations(self, rcv_station_dict):
        """
        Return all available receiver_station in database that match requirements.
        rcv_station_dict = {'city_id': int,
                            'receive_station_type': str,
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
        raise NotImplementedError
