import json

from user import User, Account

DEFAULT_ACCOUNTS_FILE = "accounts.json"
DEFAULT_USER_DATA = "users.json"


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


# Save accounts dictionary as json
def save_accounts(filepath=DEFAULT_ACCOUNTS_FILE):
    with open(filepath, mode='w', encoding="utf8") as f:
        pass


# Returns user data for given account
def read_user(account, filepath=DEFAULT_USER_DATA):
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