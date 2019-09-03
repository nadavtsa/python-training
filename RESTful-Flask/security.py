from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', 'bob1234')
]


username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}



def authenticate(username: str, password: str) -> dict:
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user



def identity(payload):
    id = payload['identity']
    return userid_mapping.get(id, None)
