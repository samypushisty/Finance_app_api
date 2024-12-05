import jwt
from core.config import settings
from fastapi import Request
from fastapi.exceptions import HTTPException


def validation(request: Request):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    if jwt_info.valid:
        return jwt_info
    else:
        raise HTTPException(status_code=500, detail=jwt_info.info_except)


def create_jwt(chat_id: int):
    return jwt.encode(payload={'id': chat_id},
                      key=settings.secret_key, algorithm='HS256')


class JwtInfo:
    def __init__(self, token: str):
        self.valid = False
        try:
            data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            self.id = data.get("id")
            self.valid =True
        except:
            self.id = None
            self.info_except = "invalid token or you haven't token"




