from fastapi import Depends, HTTPException, status
from auth.validator import is_current_access_token


def is_admin(payload: dict = Depends(is_current_access_token)):
    if payload["role"] == "admin":
        return payload
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
