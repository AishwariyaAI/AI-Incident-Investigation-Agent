from database.db import SessionLocal
from database.user_model import User


def create_user(
    username,
    password
):

    db = SessionLocal()

    user = User(
        username=username,
        password=password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    db.close()

    return user


def get_user(username):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    db.close()

    return user