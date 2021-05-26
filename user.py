# -*- coding: utf-8 -*-
from datetime import datetime

import passlib
from passlib import hash


class Account:
    __MIN_LOGIN_LENGTH = 5
    __MAX_LOGIN_LENGTH = 30
    __MIN_PASSWORD_LENGTH = 8
    __MAX_PASSWORD_LENGTH = 30

    def __init__(self, login, passwd):
        if len(login) < self.__MIN_LOGIN_LENGTH or len(login) > self.__MAX_LOGIN_LENGTH:
            raise ValueError("Login must be between {0} and {1} characters long".
                             format(self.__MIN_LOGIN_LENGTH, self.__MAX_LOGIN_LENGTH))
        self.__login = login
        if len(passwd) < self.__MIN_PASSWORD_LENGTH or len(passwd) > self.__MAX_PASSWORD_LENGTH:
            raise ValueError("Password must be between {0} and {1} characters long".
                             format(self.__MIN_PASSWORD_LENGTH, self.__MAX_PASSWORD_LENGTH))
        self.__passwd = Account.__hash_passwd(passwd)

    @property
    def login(self):
        return self.__login

    @property
    def password(self):
        return self.__passwd

    @staticmethod
    def __hash_passwd(passwd):
        return passlib.hash.sha512_crypt.hash(passwd)

    # Check if given login and password match current account
    def verify_account(self, login, password):
        if self.login != login:
            return False
        # True if encrypted password and password are identical
        return passlib.hash.sha512_crypt.verify(password, self.password)

    # Check if two account's data are identical
    @staticmethod
    def verify_account(login, password, snd_login, hashed_password):
        if login != snd_login:
            return False
        # True if encrypted password and password are identical
        return passlib.hash.sha512_crypt.verify(password, hashed_password)

    # Return account data in json format
    def to_json(self):
        account = {"login": self.login,
                   "password": self.password
                   }
        return account

class User:
    def __init__(self, account):
        self.__account = account
        self.__name = account.login
        self.__gender = True  # True - male, False - female
        self.__weight = None  # in kg
        self.__height = None  # in cm
        self.__date_of_birth = None

    def __str__(self):
        return self.name + " " + str(self.gender) + " " + str(self.weight) + " " + str(self.height) + " " + str(self.date_of_birth)

    @property
    def account(self):
        return self.__account

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        if len(new_name) == 0:
            raise ValueError("Name can't be empty")
        self.__name = new_name

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, new_gender: bool):
        self.__gender = new_gender

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, new_weight: float):
        if new_weight < 0:
            raise ValueError("Weight must be positive number")
        self.__weight = new_weight

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, new_height: float):
        if new_height < 0:
            raise ValueError("Height must be positive number")
        self.__height = new_height

    @staticmethod
    def validate_date(date):
        # date format %y-%m-%d, "DD-MM-YYYY".
        try:
            datetime.strptime(date, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, new_date):
        if User.validate_date(new_date):
            self.__date_of_birth = datetime.strptime(new_date, "%d-%m-%Y")
        else:
            raise ValueError("Date must be valid date in format DD-MM-YYYY")

    # Return user data in json format
    def to_json(self):
        if self.gender:
            gender = 'True'
        else:
            gender = 'False'
        d = self.date_of_birth
        if d is None:
            date = "01-01-2000"
        else:
            day = d.day
            if day < 10:
                day = "0" + str(day)
            else:
                day = str(day)
            month = d.month
            if month < 10:
                month = "0" + str(month)
            else:
                month = str(month)
            date = "{0}-{1}-{2}".format(day, month, d.year)
        user = {'login': self.account.login,
                'name': self.name,
                'gender': gender,
                'weight': self.weight,
                'height': self.height,
                'birthday': date
                }
        return user
