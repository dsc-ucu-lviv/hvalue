import hashlib

from database.db_base import *


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
        - IndexError
        - UserAlreadyExists
        """
        if not {'email', 'password', 'username'}.issubset(user_dict):
            raise IndexError

        try:
            self._get_user_id_by_email(user_dict['email'])
            raise UserAlreadyExists
        except UserDoesNotExists:
            pass

        # In case there are other irrelevant keys in user_dict -> creating new dict
        new_user_dict = {'email': user_dict['email'],
                         'password': self._hash_password(user_dict['password']),
                         'username': user_dict['username'],
                         'type_id': 0}

        self.increase_last_id('user_id')
        self.db.put(self.t_users, self.get_last_id('user_id'), new_user_dict)

    def check_user_password_by_email(self, email, password):
        """
        Check if user password is correct.
        user_dict = {'email': str,
                     'password': str}
        :return: user_id / False / Error
        - UserDoesNotExists
        """
        # In case user does not exists, line below will raise error
        user_id = self._get_user_id_by_email(email)

        if self.check_user_password_by_id(user_id, password):
            return user_id
        return False

    def check_user_password_by_id(self, user_id, password):
        """
        Check if user password is correct by user_id.
        :return: True / False / Error
        - UserDoesNotExists
        """
        # In case user does not exists, line below will raise error
        user_info = self._get_user_info(user_id)

        return self._hash_password(password) == user_info['password']

    def get_general_user_info(self, user_id):
        """
        Return general user info (without password hash).
        :return: (dict) {'type_id': str,
                         'username': str,
                         'email': str,
                         'phone_number': str / None} / Error
        UserDoesNotExists - invalid user_id
        """
        # In case user does not exists, line below will raise error
        user_info = self._get_user_info(user_id)

        return {'type_id': user_info['type_id'],
                'username': user_info['username'],
                'email': user_info['email'],
                'phone_number': user_info['phone_number'] if 'phone_number' in user_info else None}

    def update_general_user_info(self, user_dict):
        """
        :param user_dict: {'user_id': int,
                           'username': str,
                           'email': str,
                           'phone_number': str / None}
        :return: None / Error
        IndexError - invalid input format
        UserDoesNotExists - invalid user_id
        """
        if not {'user_id', 'username', 'email', 'phone_number'}.issubset(user_dict):
            raise IndexError

        # Check user existence
        self.get_general_user_info(user_dict['user_id'])

        # Check if provided email is unique
        try:
            some_user_id = self._get_user_id_by_email(user_dict['email'])
            if some_user_id != user_dict['user_id']:
                raise EmailIsNotUnique
        except UserDoesNotExists:
            pass

        for key in ['username', 'email', 'phone_number']:
            if user_dict[key]:
                self.db.put('{}/{}'.format(self.t_users, user_dict['user_id']), key, user_dict[key])

    def update_user_password(self, user_id, new_password):
        """
        Update user password in database.
        :param user_id: int
        :param new_password: str
        :return: None / Error
        - UserDoesNotExists
        """
        # In case user does not exists, line below will raise error
        self._get_user_info(user_id)

        self.db.put('{}/{}'.format(self.t_users, user_id), "password", self._hash_password(new_password))

    def _get_user_info(self, user_id):
        """
        :param user_id: (int)
        :return: (dict) {'user_id': int,
                         'username': str,
                         'email': str,
                         'password': str,
                         ? 'phone_number': str} / Error
        - UserDoesNotExists
        """
        users = self.db.get(self.t_users, None)
        try:
            if users[user_id] is not None:
                return users[user_id]
        except IndexError:
            pass
        raise UserDoesNotExists

    def _get_user_id_by_email(self, email):
        """
        :param email: (str)
        :return: (int) user_id / Error
        - UserDoesNotExists
        """
        users = self.db.get(self.t_users, None)
        for i, user in enumerate(users):
            if (user is not None) and (email == user['email']):
                return i
        raise UserDoesNotExists

    @staticmethod
    def _hash_password(password):
        """
        :param password: (str)
        :return: (str) hashed_password
        """
        return hashlib.sha256(str(password).encode('utf-8')).hexdigest()
