from kivy.app import App
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from filehandler import read_user
from personaltrainer import MainMenuScreen
from user import *


# Screen shown to user during login process
class LoginScreen(Screen):
    __accounts_dict = {}

    def __init__(self, accounts, **kwargs):
        super().__init__(**kwargs)
        self.__accounts_dict = accounts

    def on_size(self, *args):
        label = self.ids.get("incorrect", None)
        if label is not None:
            label.font_size = (self.height / 120 + self.width / 60) * 3

    def login(self):
        login = self.ids["login"].text
        password = self.ids["password"].text
        accounts = self.__accounts_dict

        # Check if user with given login and password exists
        for acc in accounts:
            # If login and password are correct
            if Account.verify_account(login, password, acc, accounts[acc]):
                # Load user data
                account = Account(login, password)
                user = read_user(account)
                # Unable to load user data
                if user is None:
                    App.get_running_app().stop()
                # Switch to main menu screen
                self.manager.add_widget(MainMenuScreen(user=user, name="menu-main"))
                self.manager.current = "menu-main"
                return

        # If user verification fails, display error message
        if self.ids.get("incorrect", 0) == 0:
            error_info = self.ids['login-info']
            error_label = Label(text="Incorrect login or password", color=(1, 50 / 255, 50 / 255, 1),
                                font_size=(self.height / 120 + self.width / 60) * 3)
            self.ids["incorrect"] = error_label
            error_info.add_widget(error_label)
        return


# Screen shown to user during creation of login and password
class RegisterAccountScreen(Screen):
    __accounts_dict = {}

    def __init__(self, accounts, **kwargs):
        super().__init__(**kwargs)
        self.__accounts_dict = accounts

    def on_size(self, *args):
        label = self.ids.get("incorrect", None)
        if label is not None:
            label.font_size = (self.height / 240 + self.width / 120) * 3

    def register(self):
        login = self.ids["login-create"].text
        password = self.ids["password-create"].text
        accounts = self.__accounts_dict
        "register-info"
        # Check if user with given login already exists
        if login in accounts:
            # If there is user with given login, display error message
            if self.ids.get("incorrect", 0) == 0:
                error_label = Label(text="User with given login already exists", color=(1, 50 / 255, 50 / 255, 1),
                                    font_size=(self.height / 240 + self.width / 120) * 3)
                self.ids["incorrect"] = error_label
                self.ids['register-info'].add_widget(error_label)
            return

        # If password or login are not valid
        try:
            new_account = Account(login, password)
        except ValueError as e:
            if self.ids.get("incorrect", 0) == 0:
                error_label = Label(text=str(e), color=(1, 50 / 255, 50 / 255, 1),
                                    font_size=(self.height / 240 + self.width / 120) * 3, )
                self.ids["incorrect"] = error_label
                self.ids['register-info'].add_widget(error_label)
            else:
                self.ids.get("incorrect", 0).text = str(e)
            return
        # Switch to register user screen

        # Create register user screen (part 2 of registering account)
        self.manager.add_widget(RegisterUserScreen(account=new_account, name="register-user"))
        self.manager.current = "register-user"
        return


# Screen shown to user during creation of user data
class RegisterUserScreen(Screen):
    __account = None
    __user = None
    male_box_active = BooleanProperty(True)

    def __init__(self, account, **kwargs):
        super().__init__(**kwargs)
        self.__account = account
        self.__user = User(account)
        self.ids["name-create"].text = account.login

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, new_account):
        self.__account = new_account

    def register(self):
        try:
            name = self.ids['name-create'].text
            weight = self.ids['weight-create'].text
            height = self.ids['height-create'].text
            male = self.ids['malebox'].active
            day = self.ids['day-create'].text
            month = self.ids['month-create'].text
            year = self.ids['year-create'].text
            self.__user.name = name
            if weight != "":
                self.__user.weight = int(weight)
            if height != "":
                self.__user.height = int(height)
            self.__user.gender = male
            # If all date fields are filled
            if not (day == "" or month == "" or year == ""):
                birthday = day + "-" + month + "-" + year
                self.__user.date_of_birth = birthday
            # If none of the date fields if filled
            elif day == "" and month == "" and year == "":
                pass
            # If at least one fields is not filled
            else:
                raise ValueError("Incorrect date")
        except ValueError as e:
            if self.ids.get("incorrect", 0) == 0:
                error_label = Label(text=str(e), color=(1, 50 / 255, 50 / 255, 1),
                                    font_size=(self.height / 240 + self.width / 120) * 3)
                self.ids["incorrect"] = error_label
                self.ids['register-user-info'].add_widget(error_label)
            else:
                self.ids.get("incorrect", 0).text = str(e)
            return
        self.manager.add_widget(MainMenuScreen(user=self.__user, name="menu-main"))
        self.manager.current = "menu-main"


class NumericField(TextInput):
    allowed_len = NumericProperty(0)

    # Strips any characters from widget if there are more than allowed
    # Validates if date contains only numbers
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= self.allowed_len:
            return
        if not substring.isnumeric():
            return
        self.text += substring
