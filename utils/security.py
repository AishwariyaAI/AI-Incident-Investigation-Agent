from fastapi import Header, HTTPException
from services.auth_service import SECRET_KEY
from jose import jwt

def get_current_user(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]

    except:
        raise HTTPException(status_code=401, detail="Invalid token")