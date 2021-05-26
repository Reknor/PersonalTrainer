
import vlc

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from functools import partial

import os

from kivy.uix.widget import Widget

import workouts
from workouts import Workout

# vlc path
os.add_dll_directory("C:\Program Files\VideoLAN\VLC")


# Main application menu
class MainMenuScreen(Screen):
    __user = None

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)

        # Initialize all workouts when screen loads
        workouts.initialize_data()
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
        dropdown.values = list(workouts.all_workouts)

    # Select first workout and update text
    def select_default_workout(self):
        all_workouts = workouts.all_workouts
        self.selected_workout = all_workouts[list(all_workouts)[0]]
        self.selected_workout_name = self.selected_workout.name

    # When user changes workout in dropdown menu
    def change_workout(self, widget):
        self.selected_workout = workouts.all_workouts[widget.text]
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
        sets_label = Label(text=str(workout.sets_count(difficulty)), size_hint=(1, 1), font_size=18, halign="left")
        sets_box.add_widget(sets_label)
        sets_label.bind(size=sets_label.setter('text_size'))

        time_box = BoxLayout(size_hint=(1, 1))
        time_box.add_widget(Label(text="Breaks: ", size_hint=(1, 1), font_size=18))
        # Breaks for all sets for given difficulty
        breaks_text = ""
        for b in workout.get_breaks(difficulty):
            breaks_text += str(b) + "s, "
        breaks_text = breaks_text[:len(breaks_text)-2]
        time_label = Label(text=str(breaks_text), size_hint=(1, 1), font_size=18, halign="left")
        time_box.add_widget(time_label)
        time_label.bind(size=time_label.setter('text_size'))

        sets_box.add_widget(Label(text="", size_hint=(1, 1), font_size=18))

        sets_layout.add_widget(sets_box)
        sets_layout.add_widget(time_box)
        self.add_widget(sets_layout)
        self.add_widget(Label(text=""))
        # Exercises information
        for j in range(0, len(exercises)):
            # Row box
            set_row = BoxLayout()
            set_row.add_widget(Label(text=("Set: " + str(j + 1)), size_hint=(.5, 1), font_size=18))
            self.add_widget(set_row)
            ex_num = 1
            for i in range(0, len(exercises[j])):
                # Row box
                exercise_row = BoxLayout(size_hint=(1, 1))
                # Picture placeholder
                exercise_row.add_widget(Label(text="", size_hint=(.3, 1), font_size=18))

                ex = exercises[j][i]
                # Format output depending on type

                if type(ex[0]) is workouts.Break:
                    label = Label(text="-       " + str(ex[1]) + "s    " + ex[0].name, size_hint=(1, 1), halign="left", font_size=18)
                else:
                    label = Label(text=str(ex_num) + ".    " + str(ex[1]) + "s   " + ex[0].name, size_hint=(1, 1), halign="left", font_size=18)
                    ex_num += 1

                label.bind(size=label.setter('text_size'))
                exercise_row.add_widget(label)
                self.add_widget(exercise_row)
            self.add_widget(Label(text=""))


# Displays current exercise
class ExerciseScreen(Screen):
    DEFAULT_COUNTDOWN_SOUND = "media/countdown.mp3"  # path to audio file
    DEFAULT_WORKOUT_END_SOUND = "media/end.mp3"  # path to audio file

    __workout = None  # selected workout
    __diff: int  # difficulty level
    __ex_count: int  # number of exercises on each set
    __current_ex: int  # current exercise index
    __sets_count: int  # total number of sets
    __current_set: int  # current set

    progress_max = NumericProperty(0)  # displayed in progress bar total time for current workout (for kv file)
    time_passed = NumericProperty(0)  # displayed in progress bar time from starting workout (for kv file)
    timer_prop = StringProperty("10")  # displayed timer value (for kv file)
    timer_val: int  # displayed timer value
    counter_event = None  # reference to function performed every counter tick

    __sound = None  # sound played 3 seconds before exercise or break ends

    def __init__(self, workout, diff, **kwargs):
        super().__init__(**kwargs)

        self.__workout = workout
        self.__diff = diff
        self.__current_ex = 0
        self.__current_set = 0
        self.__ex_count = len(workout.exercises(diff)[self.__current_set])
        self.__sets_count = workout.sets_count(diff)

        self.timer_val = 10
        self.progress_max = workout.get_time(diff)
        self.time_passed = 0
        self.__sound = vlc.MediaPlayer(self.DEFAULT_COUNTDOWN_SOUND)
        self.next_exercise(None)
        self.ids["current-set"].text = "Set: " + str(self.__current_set+1) + " / " + str(self.__sets_count)

    def start_exercise(self, time):
        self.start_counter(time)

    # Start next exercise, if all exercises finished move to next set
    def next_exercise(self, dt):
        # Prepare for the next exercise
        self.ids['exercise-content'].clear_widgets()
        self.stop_timer()

        # Add remaining time to progress bar
        self.time_passed += self.timer_val

        # End of set
        if self.__current_ex >= self.__ex_count:
            self.next_set()
            return
        # Get next exercise and time
        exercise, time = self.__workout.exercises(self.__diff)[self.__current_set][self.__current_ex]
        self.display_exercise(exercise)
        self.start_exercise(time)
        self.__current_ex += 1

    # Start new set, if all sets finished end workout
    def next_set(self):
        self.__current_set += 1
        # End of sets - end of workout
        if self.__current_set >= self.__sets_count:
            self.end_of_workout()
            return
        # Reset exercises
        self.__current_ex = 0
        self.__ex_count = len(self.__workout.exercises(self.__diff)[self.__current_set])
        # Display break between sets
        exercise = workouts.all_exercises["Break sets"]
        self.display_exercise(exercise)
        # Start next exercise
        self.start_exercise(self.__workout.get_break(self.__diff, self.__current_set-1))
        # Display next set
        self.ids["current-set"].text = "Set: " + str(self.__current_set+1) + " / " + str(self.__sets_count)

    # Start counting
    def start_counter(self, value):
        self.timer_prop = self.format_time(value)
        self.timer_val = value
        # Schedule every second
        self.counter_event = Clock.schedule_interval(self.update_timer, 1)

    # Stop counting and cancel audio event
    def stop_timer(self):
        if self.counter_event is not None:
            self.counter_event.cancel()
        self.__sound.stop()

    def update_timer(self, dt):
        val = self.timer_val
        # Start playing countdown sound
        if val == 3:
            Clock.schedule_once(self.play_countdown)
        # End of exercise
        elif val == 0:
            self.counter_event.cancel()
            self.counter_event = None
            Clock.schedule_once(self.next_exercise)
        self.time_passed += 1
        self.timer_val -= 1
        # Display new time
        self.timer_prop = self.format_time(val)

    # Wrapper function for playing counter sound
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

    # Show information about exercise, name, description, image
    def display_exercise(self, exercise):
        panel = self.ids["exercise-content"]
        panel.add_widget(Label(text=""))
        name = Label(text=exercise.name, font_size=36, padding=(10, 10))
        panel.add_widget(name)

        if exercise.description != "":
            description = Label(text=exercise.description, padding=(10, 10), font_size=18)
            description.text_size = (500, 150)
            panel.add_widget(description)
        if exercise.img != "img/":
            image = AsyncImage(source=exercise.img, pos_hint={'center_x': .5, 'top_y': 1}, size_hint=(None, None),
                               size=self.size)
            self.ids["ex-img"] = image
            panel.add_widget(image)
        else:
            panel.add_widget(Label(text=""))

    def on_size(self, *args):
        image = self.ids.get("ex-img", None)
        if image is not None and image.source != "img/":
            image.size = self.size

    # Move to workout end screen
    def end_of_workout(self):
        sound = vlc.MediaPlayer(self.DEFAULT_WORKOUT_END_SOUND)
        # Delete old end screen
        if self.manager.has_screen("workout-end"):
            self.manager.remove_widget(self.manager.get_screen("workout-end"))
        self.manager.add_widget(WorkoutEndScreen(name="workout-end", workout=self.__workout))
        # Play end sound
        sound.play()
        self.manager.current = "workout-end"


# Used to display progress bar for workout
class ProgressBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)
        with self.canvas.before:
            Color(78/255, 78/255, 78/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# Used to mix in background color for any widget
class BackgroundColor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)
        with self.canvas.before:
            Color(78/255, 78/255, 78/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# End of workout
class WorkoutEndScreen(Screen):
    __workout = None

    def __init__(self, workout, **kwargs):
        super().__init__(**kwargs)
        self.__workout = workout


# Profile options, data and statistics
class ProfileScreen(Screen):
    __user = None

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.__user = user
