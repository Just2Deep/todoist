from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.auth import model, service
from src.database.core import DbSession
from src.rate_limiting import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register_user(
    request: Request, register_user_request: model.RegisterUserRequest, db: DbSession
):
    """
    Register a new user.
    """
    service.register_user(db=db, user_data=register_user_request)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=model.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbSession,
) -> model.Token:
    """
    Authenticate a user and return an access token.
    """
    return service.login_for_access_token(form_data=form_data, db=db)
