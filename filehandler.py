import json

from user import User
import workouts

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
                accounts_dict[data[account]['login']] = data[account]['password']
            return accounts_dict
    except (IOError, FileNotFoundError, OSError, ValueError):
        return None


# Save current user account
def save_account(account, filepath=DEFAULT_ACCOUNTS_FILE):
    try:
        # Read all user data
        with open(filepath, mode='r', encoding="utf8") as f:
            data = json.load(f)
            print(data)
            print("hm")
        # Append new user
        with open(filepath, mode='w', encoding="utf8") as f:
            data[account.login] = account.to_json()
            print(data)
            json.dump(data, f, indent=4)
            return True
        return False
    except (IOError, FileNotFoundError, OSError, ValueError) as e:
        print(e)
        return False

# Save current user data
def save_user(user, filepath=DEFAULT_USER_FILE):
    try:
        # Read all user data
        with open(filepath, mode='r', encoding="utf8") as f:
            data = json.load(f)
            print(data)
            print("hm")
        # Append new user
        with open(filepath, mode='w', encoding="utf8") as f:
            try:
                data[user.name] = user.to_json()
                print(data)
                save_account(user.account)
                json.dump(data, f, indent=4)
                return True
            except (ValueError, AttributeError) as e:
                print(data)
                print(e)
                return False
    except (IOError, FileNotFoundError, OSError, ValueError) as e:
        print(e)
        return False


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
                    if user['weight'] is None:
                        u.weight = 0
                    else:
                        u.weight = int(user['weight'])
                    if user['height'] is None:
                        u.height = 0
                    else:
                        u.height = int(user['height'])
                    u.date_of_birth = user['birthday']
                    return u
            return None
    except (IOError, FileNotFoundError, OSError, ValueError)as e:
        return None


# Read all exercises
def read_exercises(filepath=DEFAULT_EXERCISES_FILE):
    try:
        with open(filepath, mode='r', encoding="utf8") as f:
            exercises = {}
            data = json.load(f)
            for d in data['exercises']:
                if d['name'].lower().startswith("break"):
                    e = workouts.Break(d)
                else:
                    e = workouts.Exercise(d)
                exercises[e.name] = e
            return exercises
    except (IOError, FileNotFoundError, OSError, ValueError):
        return None


# Read all workouts, remember to call read_exercises before or workout initialization will fail
def read_workouts(filepath=DEFAULT_WORKOUTS_FILE):
    try:
        with open(filepath, mode='r', encoding="utf8") as f:
            workouts_dict = {}
            data = json.load(f)
            for d in data['workouts']:
                w = workouts.Workout(d)
                workouts_dict[w.name] = w
            return workouts_dict
    except (IOError, FileNotFoundError, OSError, ValueError):
        return None