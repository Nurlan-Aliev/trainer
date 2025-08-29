from fastapi import status, Request, Response
from auth.schemas import UserAuthSchema
from auth import jwt_helper
from fastapi.responses import RedirectResponse


def sign_in(response:Response, user: UserAuthSchema):

    access_token = jwt_helper.create_jwt(user)
    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=False,
        httponly=True,
        max_age=3600,
    )
    response.status_code = 200

    return response
