import json


# This function takes in a username and password, and will access the users.json file.
# It opens the json file and compares it to
def authenticate_user(username, password, users_file="users.json"):
    with open(users_file, "r") as f:
        users = json.load(f)
    user = users.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None
