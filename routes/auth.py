from fastapi import APIRouter

from schemas.auth import (
    UserRegister,
    UserLogin
)

from services.auth_service import (
    register_user,
    authenticate,
    create_token
)

router = APIRouter()


@router.post("/register")
def register(data: UserRegister):

    register_user(
        data.username,
        data.password
    )

    return {"message": "Registered"}


@router.post("/login")
def login(data: UserLogin):

    valid = authenticate(
        data.username,
        data.password
    )

    if not valid:
        return {"error": "Invalid Login"}

    token = create_token(
        data.username
    )

    return {
        "access_token": token
    }