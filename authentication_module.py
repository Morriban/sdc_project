import json

def authenticate_user(username, password, users_file="users.json"):
    with open(users_file, "r") as f:
        users = json.load(f)
    user = users.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None
