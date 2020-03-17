from database.db_base import DBBase


class DBLocations(DBBase):
    def __init__(self, database):
        super().__init__(database)

        self.t_cities = '/cities'
        self.t_locations = '/locations'

    def get_cities(self):
        """
        Return all available cities in database.
        :return: (dict) {city_id: "city_name", ...}
        """
        return self.db.get(self.t_cities, None)

    def get_location_info(self, city_id, location_id):
        """
        Returns location info.
        :param city_id: (int)
        :param location_id: (int)
        :return: (dict) { "location_id": int,
                          "address": str,
                          "latitude": float,
                          "longitude": float } / Error
        KeyError - wrong city_id
        IndexError - wrong location_id
        """
        self._get_city_name(city_id)

        location_info = self.db.get('{}/{}/{}'.format(self.t_locations, city_id, location_id), None)
        if location_info is None:
            raise IndexError
        return location_info

    def get_locations(self, city_id):
        """
        Return all locations by city_id.
        :param city_id: (int)
        :return: [ {"location_id": int,
                    "address": str,
                    "latitude": float,
                    "longitude": float } , ...] / Error
        KeyError - wrong city_id
        """
        self._get_city_name(city_id)

        return self.db.get('{}/{}'.format(self.t_locations, city_id), None)

    def add_new_location(self, location_dict):
        """
        Add new location to the database.
        :param location_dict: (dict) {"city_id": (int),
                                      "address": (str)}
        :return: location_id / Error
        IndexError -- invalid format of input data.
        KeyError -- wrong city_id.

        """
        if not {'city_id', 'address'}.issubset(location_dict):
            raise IndexError

        city_id = location_dict['city_id']

        # Returns error if wrong city_id.
        lat, lon = self.get_coordinates_from_address(city_id, location_dict['address'])
        new_location_dict = {'address': location_dict['address'],
                             'latitude': lat,
                             'longitude': lon}

        self.increase_last_id('{}/{}'.format('location_id', city_id))
        self.db.put('{}/{}'.format(self.t_locations, city_id),
                    self.get_last_id('{}/{}'.format('location_id', city_id)),
                    new_location_dict)

    def get_coordinates_from_address(self, city_id, address):
        """
        Return coordinates of given address using Google Maps API.
        :param address: (str) example: "Kozelnytska 2a"
        :return: (latitude, longitude)
        """
        self._get_city_name(city_id)
        # TODO (issue #33): return right coordinates
        # Return some error or default coordinates, if the address is invalid
        return (49.841888, 24.030108)

    def _get_city_name(self, city_id):
        """
        :param city_id: (int)
        :return: (str) / Error
        KeyError -- city does not exists
        """
        cities = self.get_cities()
        try:
            if cities[city_id] is None:
                return KeyError
        except IndexError:
            raise KeyError
        return cities[city_id]
