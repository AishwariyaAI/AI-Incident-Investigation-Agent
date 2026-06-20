from jose import jwt

from database.user_crud import (
    create_user,
    get_user
)
SECRET_KEY = "dev123"


def register_user(
    username,
    password
):

    existing = get_user(username)

    if existing:
        return False

    create_user(
        username,
        password
    )

    return True


def authenticate(
    username,
    password
):

    user = get_user(username)

    if not user:
        return False

    return (
        user.password == password
    )


def create_token(username):

    return jwt.encode(
        {"sub": username},
        SECRET_KEY,
        algorithm="HS256"
    )