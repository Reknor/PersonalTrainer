import json

from user import User, Account
from workouts import Exercise, Workout, Break

DEFAULT_ACCOUNTS_FILE = "data/accounts.json"
DEFAULT_USER_FILE = "data/users.json"
DEFAULT_EXERCISES_FILE = "data/exercises.json"
DEFAULT_WORKOUTS_FILE = "data/workouts.json"


# Returns dictionary (login, password)
def read_accounts(filepath=DEFAULT_ACCOUNTS_FILE):
    try:
        with open(filepath, mode='r', encoding="utf8") as f:
            data = json.load(f)
            accounts_dict = {}
            for account in data:
                # print(data[account]['login'])
                # print(data[account]['password'])
                accounts_dict[data[account]['login']] = data[account]['password']
            # print(accounts_dict)
            return accounts_dict
    except (IOError, FileNotFoundError, OSError, ValueError):
        return None


# Returns user data for given account
def read_user(account, filepath=DEFAULT_USER_FILE):
    try:
        with open(filepath, mode='r', encoding="utf8") as f:
            data = json.load(f)
            for user in data:
                if data[user]['login'] == account.login:
                    user = data[user]
                    u = User(account)
                    u.name = user['name']
                    u.gender = bool(user['gender'])
                    u.weight = int(user['weight'])
                    u.height = int(user['height'])
                    u.date_of_birth = user['birthday']
                    return u
            return None
    except (IOError, FileNotFoundError, OSError, ValueError):
        return None


# Read all exercises
def read_exercises(filepath=DEFAULT_EXERCISES_FILE):
    try:
        with open(filepath, mode='r', encoding="utf8") as f:
            exercises = {}
            data = json.load(f)
            for d in data['exercises']:
                if d['name'].lower().startswith("break"):
                    e = Break(d)
                else:
                    e = Exercise(d)
                exercises[e.name] = e
            return exercises
    except (IOError, FileNotFoundError, OSError, ValueError):
        return None


# Read all workouts, remember to call read_exercises before or workout initialization will fail
def read_workouts(filepath=DEFAULT_WORKOUTS_FILE):
    try:
        with open(filepath, mode='r', encoding="utf8") as f:
            workouts = {}
            data = json.load(f)
            for d in data['workouts']:
                w = Workout(d)
                workouts[w.name] = w
            return workouts
    except (IOError, FileNotFoundError, OSError, ValueError):
        return None

