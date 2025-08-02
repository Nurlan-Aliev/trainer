from fastapi import status, Request
from auth.schemas import UserAuthSchema
from auth import jwt_helper
from fastapi.responses import RedirectResponse


def sign_in(request: Request, user: UserAuthSchema):

    access_token = jwt_helper.create_jwt(user)
    redirect_url = request.url_for("get_home_page")
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=False,
        httponly=True,
        max_age=3600,
    )

    return response
