from kivy.app import App
from kivy.uix.screenmanager import Screen


# Main application menu
class MainMenuScreen(Screen):
    __user = None

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.__user = user

    @staticmethod
    def exit():
        App.get_running_app().stop()
