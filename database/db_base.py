class DBBase:
    def __init__(self, database):
        self.db = database

    def get_last_id(self, table_name):
        return self.db.get('last_id/{}'.format(table_name), None)

    def increase_last_id(self, table_name):
        last_id = self.db.get('last_id/{}'.format(table_name), None)
        if last_id is not None:
            self.db.put('last_id/', table_name, last_id + 1)
        else:
            raise IndexError

    @staticmethod
    def valid_date_format(date):
        """
        Check if date format is 'YYYY-MM-DD'.
        :param date: str
        :return: True / False
        """
        try:
            date = date.split('-')
            assert len(date[0]) == 4, None
            assert len(date[1]) == 2, None
            assert len(date[2]) == 2, None

            assert int(date[1]) < 13, None
            assert int(date[2]) < 32, None

            return True
        except (IndexError, AssertionError):
            return False
        
    @staticmethod
    def compare_dates(date1, date2):
        """
        Return 1 if data1 > data2, -1 if data1 < data2 and 0 if they are the same
        :param date1: (str) "2020-12-01"
        :param date2: (str) "2020-11-31"
        :return: (int) / Error
        """
        if not (DBBase.valid_date_format(date1) and DBBase.valid_date_format(date2)):
            raise TypeError

        date1 = date1.split('-')
        date2 = date2.split('-')

        for date_1, date_2 in zip(date1, date2):
            if date_1 > date_2:
                return 1
            elif date_1 < date_2:
                return -1
        return 0
