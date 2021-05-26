import filehandler

# Contains all available exercises, every exercise has unique name which is a key in dictionary
all_exercises = {}
# Contains all available workouts, every workout has unique name which is a key in dictionary
all_workouts = {}


class Exercise:
    __name: str
    __description: str
    __img: str  # Relative path to image

    # Initialize exercise from json object
    def __init__(self, json):
        self.__name = json['name']
        self.__description = json['description']
        self.__img = json['img']

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if new_name == "":
            raise ValueError("Exercise name cannot be empty")
        self.__name = new_name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, new_description):
        self.__description = new_description

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, new_img):
        self.__img = new_img


# Break between exercises marker
class Break(Exercise):
    pass


class Workout:
    __MINIMUM_DURATION_LENGTH = 10  # Minimum required exercise duration in seconds
    __MINIMUM_SETS_BREAK = 10  # Minimum required time between sets in seconds

    # Difficulty levels
    DIFF_BEGINNER = 0
    DIFF_INTERMEDIATE = 1
    DIFF_ADVANCED = 2
    DIFF_PRO = 3

    __name: str
    __difficulty: list[int]  # List of available difficulties for this workout
    __description: str

    # Dictionary with 2 key types:
    # sets_breaks_n - list of ints (break between sets in seconds), n is difficulty number
    # sets_n - list of list of pairs <exercise, duration>, n is difficulty number
    __exercises: dict

    # Initialize workouts from json object
    def __init__(self, json):
        self.__name = json['name']
        self.__difficulty = json['difficulty']
        self.__exercises = {}
        # Read breaks and exercises information
        for diff in self.__difficulty:
            b = 'sets_breaks_' + str(diff)
            self.__exercises[b] = json[b]
            # For every set
            set_list = []
            for ex_set in json['sets_' + str(diff)]:
                ex_list = []
                # For every exercise
                for i in range(0, len(ex_set), 2):
                    # Map exercise name with exercise and duration
                    pair = (all_exercises[ex_set[i]], ex_set[i+1])
                    # Add exercise and duration to one set
                    ex_list.append(pair)
                # Add set to all sets
                set_list.append(ex_list)
            # Add set to difficulty
            self.__exercises['sets_' + str(diff)] = set_list
        self.__description = json['description']

    def __str__(self):
        text = self.name + " difficulties: " + str(len(self.__difficulty)) + "\n"
        i = 0
        for k in self.__exercises.keys():
            if i % 2 == 0:
                text += "Breaks: "
            exercises_list = self.__exercises[k]
            for exercise in exercises_list:
                text += str(exercise) + ", "
            text += "\n"
            i += 1
        return text

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if new_name == "":
            raise ValueError("Workout name cannot be empty")
        self.__name = new_name

    def sets_count(self, diff):
        return len(self.__exercises["sets_" + str(diff)])

    def get_break(self, difficulty, set_num):
        return self.__exercises["sets_breaks_" + str(difficulty)][set_num]

    def get_breaks(self, difficulty):
        return self.__exercises["sets_breaks_" + str(difficulty)]

    @property
    def all_breaks(self):
        breaks = []
        for diff in self.__difficulty:
            breaks.append(self.__exercises["sets_breaks_" + str(diff)])
        return breaks

    def sets_break(self, set_num):
        return self.__exercises["sets_breaks_" + str(set_num)]

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, new_description):
        self.__description = new_description

    @property
    def all_exercises(self):
        return self.__exercises

    def exercises(self, difficulty):
        if difficulty not in self.__difficulty or difficulty < 0:
            return None
        return self.__exercises["sets_" + str(difficulty)]

    # Returns total time required to finish workout
    def get_time(self, difficulty):
        total_time = 0
        exercises = self.exercises(difficulty)
        breaks = self.get_breaks(difficulty)
        i = 0
        for li in exercises:
            for e in li:
                total_time += e[1]
            total_time += breaks[i]
            i += 1
        return total_time

    # Returns pair <value, text> describing available difficulties for workout
    def get_difficulties(self):
        diff = []
        for i in self.__difficulty:
            if i == 0:
                text = "Beginner"
            elif i == 1:
                text = "Intermediate"
            elif i == 2:
                text = "Advanced"
            else:
                text = "Professional"
            diff.append((i, text))
        return diff

    # Returns difficulty value based on text
    @staticmethod
    def get_difficulty(difficulty: str):
        if difficulty == "Beginner":
            return 0
        elif difficulty == "Intermediate":
            return 1
        elif difficulty == "Advanced":
            return 2
        else:  # "Professional"
            return 3


# Read exercises and workouts from files
def initialize_data():
    global all_exercises
    global all_workouts
    all_exercises = filehandler.read_exercises()
    all_workouts = filehandler.read_workouts()
    return all_exercises, all_workouts
