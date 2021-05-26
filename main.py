# -*- coding: utf-8 -*-
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from prelogin import *
from filehandler import *


# Entry application screen
class MainLoginScreen(Screen):
    __accounts_dict = {}

    def __init__(self, accounts, **kwargs):
        super().__init__(**kwargs)
        self.__accounts_dict = accounts

    @staticmethod
    def exit():
        App.get_running_app().stop()


# Main application class
class PersonalTrainer(App):

    MINIMUM_APP_WIDTH = 500
    MINIMUM_APP_HEIGHT = 500

    def build(self):
        Window.minimum_width = self.MINIMUM_APP_WIDTH
        Window.minimum_height = self.MINIMUM_APP_HEIGHT

        # Read accounts data
        accounts_dict = read_accounts()
        if accounts_dict is None:
            App.get_running_app().stop()
        # Create screen manager
        screen_manager = ScreenManager(transition=SlideTransition(direction="down"))

        # Create main menu before login
        screen_manager.add_widget(MainLoginScreen(accounts=accounts_dict, name="menu-login"))
        # Create login screen
        screen_manager.add_widget(LoginScreen(accounts=accounts_dict, name="login"))
        # Create register account screen
        screen_manager.add_widget(RegisterAccountScreen(accounts=accounts_dict, name="register-account"))
        return screen_manager


# Entry point for application
def main():
    PersonalTrainer().run()


if __name__ == "__main__":
    main()
