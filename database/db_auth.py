import hashlib

from database.db_base import DBBase


class DBAuth(DBBase):
    def __init__(self, database):
        super().__init__(database)

        self.t_users = '/users'
        self.t_user_types = '/user_types'
        self.t_last_id = '/last_id'

    def add_new_user(self, user_dict):
        """
        Create new user in database.
        user_dict = {'email': str,
                     'password': str,
                     'username': str}
        :return: user_id / Error
        """
        if not {'email', 'password', 'username'}.issubset(user_dict):
            raise IndexError

        if self._get_user_info(user_dict['email']) is not None:
            raise UserAlreadyExists

        # In case there other irrelevant keys in user_dict -> creating new dict
        new_user_dict = {'email': user_dict['email'],
                         'password': hashlib.sha256(str(user_dict['password']).encode('utf-8')).hexdigest(),
                         'username': user_dict['username'],
                         'type_id': 0}

        self.increase_last_id('user_id')
        self.db.put(self.t_users, self.get_last_id('user_id'), new_user_dict)

    def check_user_password(self, user_dict):
        """
        Check if user password is correct.
        user_dict = {'email': str,
                     'password': str}
        :return: user_id / None
        """
        if not {'email', 'password'}.issubset(user_dict):
            raise IndexError

        user_info = self._get_user_info(user_dict['email'])
        if user_info is None:
            raise UserDoesNotExists

        if hashlib.sha256(str(user_dict['password']).encode('utf-8')).hexdigest() == user_info[1]['password']:
            return user_info[0]

    def _get_user_info(self, email):
        users = self.db.get(self.t_users, None)
        for i, user in enumerate(users):
            if (user is not None) and (email == user['email']):
                return i, user


class UserAlreadyExists(Exception):
    pass


class UserDoesNotExists(Exception):
    pass
