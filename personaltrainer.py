from tkinter import Tk

import vlc
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from functools import partial
import os
from workouts import *

# Dictionary of all exercises, every exercise has unique name which is a key in dictionary
all_exercises = {}
# Dictionary of all workouts, every workout has unique name which is a key in dictionary
all_workouts = {}


# Create all exercises
def initialize_exercises():
    all_exercises["Break"] = Break("Break", None, None)

    all_exercises["Basic push ups"] = Exercise("Basic push ups", "", None)
    all_exercises["Knee plank-ups"] = Exercise("Knee plank-ups", "", None)
    all_exercises["Side step push ups"] = Exercise("Side step push ups", "", None)
    all_exercises["Prowler push ups"] = Exercise("Prowler push ups", "", None)
    all_exercises["Cliffhanger push ups"] = Exercise("Cliffhanger push ups", "", None)

    all_exercises["Basic pull ups"] = Exercise("Basic pull ups", "", None)
    all_exercises["Chin ups"] = Exercise("Chin ups", "", None)
    all_exercises["1/2 pull ups"] = Exercise("1/2 pull ups", "", None)
    all_exercises["Hanging bat pull ups"] = Exercise("Hanging bat pull ups", "", None)
    all_exercises["Angled pull ups"] = Exercise("Angled pull ups", "", None)
    all_exercises["Commando pull ups"] = Exercise("Commando  pull ups", "", None)
    all_exercises["Spiderman pull ups"] = Exercise("Spiderman  pull ups", "", None)
    all_exercises["Switch grip pull ups"] = Exercise("Switch grip pull ups", "", None)
    all_exercises["Front lever pull ups"] = Exercise("Front lever pull ups", "", None)
    all_exercises["One arm pull ups"] = Exercise("One arm pull ups", "", None)
    all_exercises["Plyo pull ups"] = Exercise("Plyo pull ups", "", None)


# Create all workouts
def initialize_workouts():
    # First initialize exercises
    initialize_exercises()
    # Difficulties aliases
    b = Workout.DIFF_BEGINNER
    a = Workout.DIFF_ADVANCED
    i = Workout.DIFF_INTERMEDIATE
    p = Workout.DIFF_PRO
    # Exercises alias
    ex = all_exercises

    w1 = Workout("Push ups variations", 3, 180, "No equipment needed")
    w1.add_exercise(b, ex["Basic push ups"], 40)
    w1.add_exercise(b, ex["Break"], 20)
    w1.add_exercise(b, ex["Knee plank-ups"], 40)
    w1.add_exercise(b, ex["Break"], 20)
    w1.add_exercise(b, ex["Side step push ups"], 40)
    w1.add_exercise(b, ex["Break"], 20)
    w1.add_exercise(b, ex["Prowler push ups"], 40)
    w1.add_difficulty_level()
    w1.add_exercise(i, ex["Basic push ups"], 55)
    w1.add_exercise(i, ex["Break"], 20)
    w1.add_exercise(i, ex["Knee plank-ups"], 55)
    w1.add_exercise(i, ex["Break"], 20)
    w1.add_exercise(i, ex["Side step push ups"], 55)
    w1.add_exercise(i, ex["Break"], 20)
    w1.add_exercise(i, ex["Cliffhanger push ups"], 55)
    all_workouts["Push ups variations"] = w1

    w2 = Workout("Pull ups variations", 3, 300,
                 "Workout requires pull up bar and some other equipment depending on exercise")
    w2.add_exercise(b, ex["Basic pull ups"], 30)
    w2.add_exercise(b, ex["Break"], 60)
    w2.add_exercise(b, ex["1/2 pull ups"], 30)
    w2.add_exercise(b, ex["Break"], 60)
    w2.add_exercise(b, ex["Chin ups"], 40)
    w2.add_exercise(b, ex["Break"], 60)
    w2.add_exercise(b, ex["Basic push ups"], 30)
    w2.add_exercise(b, ex["Break"], 60)
    w2.add_exercise(b, ex["Chin ups"], 30)
    w2.add_exercise(b, ex["Break"], 60)
    all_workouts["Pull ups variations"] = w2


# Main application menu
class MainMenuScreen(Screen):
    __user = None

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.__user = user
        Clock.schedule_once(partial(self.__create_child_screens, user), 1)

    def __create_child_screens(self, user, *largs):
        self.manager.add_widget(ProfileScreen(user=user, name="profile"))
        self.manager.add_widget(WorkoutsScreen(name="workouts"))

    # Switch to profile screen
    def go_to_profile(self):
        self.manager.current = "profile"

    # Exit application
    @staticmethod
    def exit():
        App.get_running_app().stop()


# Workouts screen
class WorkoutsScreen(Screen):

    # Default selected workout
    selected_workout = None
    # Default selected difficulty
    selected_difficulty = 0

    # Selected difficulty name displayed in dropdown
    selected_workout_diff = StringProperty("Beginner")
    # Selected workout name displayed in dropdown
    selected_workout_name = StringProperty("Select workout")
    # List of possible difficulties in dropdown
    difficulties_list = ListProperty(["Select difficulty"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize all workouts when screen loads
        initialize_workouts()

        # Select first workout by default
        self.select_default_workout()

        # Update all possible workouts
        self.update_workouts_dropdown()

        # Get all difficulties for selected workout
        self.update_difficulties()

    def update_difficulties(self):
        diff_list = []
        pairs = self.selected_workout.get_difficulties()
        for p in pairs:
            diff_list.append(p[1])
        self.difficulties_list = diff_list

        # Must check if new workout has previous difficulty, if not change to Beginner
        if self.selected_workout_diff not in diff_list:
            self.selected_workout_diff = diff_list[0]
            dropdown = self.ids["select-difficulty"]
            dropdown.text = self.selected_workout_diff

    # Update dropdown menu to match workouts dict
    def update_workouts_dropdown(self):
        dropdown = self.ids["select-workout"]
        dropdown.values = list(all_workouts)

    # Select first workout and update text
    def select_default_workout(self):
        self.selected_workout = all_workouts[list(all_workouts)[0]]
        self.selected_workout_name = self.selected_workout.name

    # When user changes workout in dropdown menu
    def change_workout(self, widget):
        self.selected_workout = all_workouts[widget.text]
        self.update_difficulties()
        # Change workout display
        workout_display = self.ids["workout-display"]
        workout_display.show(self.selected_workout, self.selected_difficulty)

    def change_difficulty(self, widget):
        difficulty = Workout.get_difficulty(widget.text)
        self.selected_difficulty = difficulty
        self.selected_workout_diff = widget.text
        workout_display = self.ids["workout-display"]
        workout_display.show(self.selected_workout, self.selected_difficulty)

    # Start selected workout
    def start_workout(self):
        # Delete old exercise screen
        if self.manager.has_screen("exercise"):
            self.manager.remove_widget(self.manager.get_screen("exercise"))
        self.manager.add_widget(ExerciseScreen(workout=self.selected_workout, diff=self.selected_difficulty, name="exercise"))
        self.manager.current = "exercise"


# Used to display selected workout
class WorkoutDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super(WorkoutDisplay, self).__init__(**kwargs)

    def show(self, workout, difficulty):
        # Get all exercises for given difficulty
        exercises = workout.exercises(difficulty)

        # Remove all previously shown items
        self.clear_widgets()
        self.spacing = dp(40)
        # Display information about workout
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=workout.name, font_size=36))
        self.add_widget(Label(text=workout.description, font_size=18))
        # Set amount and time information
        sets_layout = BoxLayout()
        sets_box = BoxLayout(size_hint=(1, 1))
        sets_box.add_widget(Label(text="", size_hint=(1, 1), font_size=18))
        sets_box.add_widget(Label(text="Sets : ", size_hint=(1, 1), font_size=18))
        # Label displaying value
        sets_label = Label(text=str(workout.sets), size_hint=(1, 1), font_size=18, halign="left")
        sets_box.add_widget(sets_label)
        sets_label.bind(size=sets_label.setter('text_size'))

        time_box = BoxLayout(size_hint=(1, 1))
        time_box.add_widget(Label(text="Time: ", size_hint=(1, 1), font_size=18))
        time_label = Label(text=str(workout.sets_break), size_hint=(1, 1), font_size=18, halign="left")
        time_box.add_widget(time_label)

        time_label.bind(size=time_label.setter('text_size'))

        sets_box.add_widget(Label(text="", size_hint=(1, 1), font_size=18))

        sets_layout.add_widget(sets_box)
        sets_layout.add_widget(time_box)
        self.add_widget(sets_layout)
        self.add_widget(Label(text=""))
        # Exercises information
        for i in range(0, len(exercises)):
            # Row box
            exercise_row = BoxLayout()
            # Picture placeholder
            exercise_row.add_widget(Label(text="", size_hint=(None, 1), width=dp(100), font_size=18))

            ex = exercises[i]
            # Format output depending on type
            if type(ex[0]) is Break:
                label = Label(text="-            " + str(ex[1]) + "s    " + ex[0].name, size_hint=(1, 1), halign="left", font_size=18)
            else:
                label = Label(text=str(int(i/2)+1) + ".    " + str(ex[1]) + "s   " + ex[0].name, size_hint=(1, 1), halign="left", font_size=18)

            label.bind(size=label.setter('text_size'))
            exercise_row.add_widget(label)
            self.add_widget(exercise_row)
        self.add_widget(Label(text=""))


# Displays current exercise
class ExerciseScreen(Screen):
    __workout = None
    __diff = 0
    __ex_count = 0
    __current_ex = 0
    __sound = None

    timer_prop = StringProperty("10")
    timer_val = 10
    counter_event = None

    def __init__(self, workout, diff, **kwargs):
        super().__init__(**kwargs)
        self.__workout = workout
        self.__diff = diff
        self.__ex_count = len(workout.exercises(diff))
        self.start_counter(70)
        self.__sound = vlc.MediaPlayer("countdown10.mp3")
        self.__sound.play()

    def start_counter(self, value):
        self.timer_prop = self.format_time(value)
        self.timer_val = value
        # Every second
        self.counter_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        val = self.timer_val
        if val == 3:
            Clock.schedule_once(self.play_countdown)
        elif val == 0:
            self.counter_event.cancel()
        self.timer_val -= 1
        self.timer_prop = self.format_time(val)

    def play_countdown(self, dt):
        self.__sound.play()

    def format_time(self, value):
        if value > 59:
            if value % 60 < 10:
                return str(int(value / 60)) + ":0" + str(value % 60)
            else:
                return str(int(value / 60)) + ":" + str(value % 60)
        else:
            return str(value)

    def display_exercise(self):
        pass


# Profile options, data and statistics
class ProfileScreen(Screen):
    __user = None

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.__user = user
