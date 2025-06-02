from typing import Annotated
from fastapi import Depends, Request, APIRouter
from starlette import status
from . import model
from . import service
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import DbSession
from ..rate_limiting import limiter


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=model.Token)
@limiter.limit("5/hour")
async def register_user(
    request: Request, register_user_request: model.RegisterUserRequest, db: DbSession
) -> model.Token:
    """
    Register a new user.
    """
    return service.register_user(db=db, user_data=register_user_request)


@router.post("/token", response_model=model.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(service.oauth2_bearer)],
    db: DbSession,
) -> model.Token:
    """
    Authenticate a user and return an access token.
    """
    return service.login_for_access_token(form_data=form_data, db=db)
