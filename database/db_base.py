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
