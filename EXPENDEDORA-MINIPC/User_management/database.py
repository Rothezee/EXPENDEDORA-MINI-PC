import json
import os

DB_FILE = 'users.json'

def load_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(DB_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def add_user(username, password):
    users = load_users()
    users.append({'username': username, 'password': password})
    save_users(users)

def get_user(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None