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
    def compare_dates(date1, date2):
        """
        Return 1 if data1 > data2, -1 if data1 < data2 and 0 if they are the same
        :param date1: (str) "2020-12-01"
        :param date2: (str) "2020-11-31"
        :return: (int)
        """
        date1 = date1.split('-')
        date2 = date2.split('-')

        for date_1, date_2 in zip(date1, date2):
            if date_1 > date_2:
                return 1
            elif date_1 < date_2:
                return -1
        return 0
