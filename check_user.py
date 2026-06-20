# check_user.py

from database.user_crud import get_user

user = get_user("admin")

print(user)