from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import model
from src.exceptions import (
    UserNotFoundError,
    InvalidPasswordError,
    PasswordMismatchError,
)
from src.auth.service import verify_password, get_password_hash
from src.entities.user import User
import logging


def get_user_by_id(db, user_id: UUID):
    """
    Retrieve a user by their ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.error(f"User with ID {user_id} not found.")
        raise UserNotFoundError(f"User with ID {user_id} not found.")

    logging.info(f"User with ID {user_id} retrieved successfully.")
    return user


def change_password(
    db: Session, user_id: UUID, password_change: model.PasswordChangeRequest
) -> None:
    """
    Change the password for a user.
    """
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            logging.error(f"User with ID {user_id} not found.")
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        if not verify_password(password_change.current_password, user.password):
            logging.error("Current password is incorrect.")
            raise InvalidPasswordError("Current password is incorrect.")

        if password_change.new_password != password_change.new_password_confirmation:
            logging.error("New password and confirmation do not match.")
            raise PasswordMismatchError("New password and confirmation do not match.")

        user.password = get_password_hash(password_change.new_password)
        db.commit()
        return None
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        raise
