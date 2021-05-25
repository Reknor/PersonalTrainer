class Exercise:

    __name: str
    __description: str
    __img: str  # Relative path to image

    def __init__(self, name, description, img):
        self.__name = name
        self.__description = description
        self.__img = img

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
    __sets: int  # How many times all exercises are repeated
    __sets_break: int  # Time between sets in seconds
    __description: str
    # List of  pairs <exercise, duration> lists, each list contains exercises for one difficulty level, 0 - easiest
    __exercises: [[]]

    def __init__(self, name, sets, s_break, description):
        self.__name = name
        self.__sets = sets
        self.__sets_break = s_break
        self.__description = description
        self.__exercises = [[]]

    def __str__(self):
        text = self.name + " sets: " + str(self.sets) + "\n"
        for exercises_list in self.all_exercises:
            for exercise in exercises_list:
                text += str(exercise) + ", "
            text += "\n"
        return text

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if new_name == "":
            raise ValueError("Workout name cannot be empty")
        self.__name = new_name

    @property
    def sets(self):
        return self.__sets

    @sets.setter
    def sets(self, new_sets: int):
        if new_sets <= 0:
            raise ValueError("Number of sets must be positive")
        self.__sets = new_sets

    @property
    def sets_break(self):
        return self.__sets_break

    @sets_break.setter
    def sets_break(self, new_break):
        if new_break <= self.__MINIMUM_SETS_BREAK:
            raise ValueError("Break between sets must be longer than {0}s".format(self.__MINIMUM_SETS_BREAK))

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
        if difficulty >= len(self.__exercises) or difficulty < 0:
            return None
        return self.__exercises[difficulty]

    def add_exercise(self, difficulty, exercise, duration):
        if difficulty >= len(self.__exercises) or difficulty < 0:
            return False
        if duration <= self.__MINIMUM_DURATION_LENGTH:
            raise ValueError("Exercise duration must be greater than {0}s".format(self.__MINIMUM_DURATION_LENGTH))
        self.__exercises[difficulty].append((exercise, duration))
        return True

    def add_difficulty_level(self):
        # Maximum difficulty level reached
        if len(self.__exercises) >= 4:
            return False
        self.__exercises.append([])
        return True

    # Returns pair <value, text> describing available difficulties for workout
    def get_difficulties(self):
        diff = []
        for i in range(0, len(self.all_exercises)):
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