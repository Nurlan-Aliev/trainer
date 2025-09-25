from fastapi import Response
import json
from auth.schemas import UserAuthSchema
from auth import jwt_helper


def sign_in(user: UserAuthSchema):
    access_token = jwt_helper.create_access_token(user)
    refresh_token = jwt_helper.create_refresh_token(user)
    response: Response = Response(content=json.dumps(access_token))
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        secure=False,
        httponly=True,
        max_age=3600,
    )
    response.status_code = 200
    return response
