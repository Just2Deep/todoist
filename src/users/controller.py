from fastapi import APIRouter, status

from src.database.core import DbSession
from src.users import model, service
from src.auth.service import CurrentUser


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=model.UserResponse)
async def get_current_user(
    current_user: CurrentUser, db: DbSession
) -> model.UserResponse:
    """
    Retrieve the currently authenticated user.
    """
    return service.get_user_by_id(db=db, user_id=current_user.get_uuid())


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_change: model.PasswordChangeRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    """
    Change the password for the currently authenticated user.
    """
    service.change_password(
        db=db, user_id=current_user.get_uuid(), password_change=password_change
    )
