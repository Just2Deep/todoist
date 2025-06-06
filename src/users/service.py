import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.auth.service import get_password_hash, verify_password
from src.entities.user import User
from src.exceptions import (
    InvalidPasswordError,
    PasswordMismatchError,
    UserNotFoundError,
)
from src.users import model


def get_user_by_id(db, user_id: UUID) -> User:
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

        if not verify_password(password_change.current_password, user.hashed_password):
            logging.error("Current password is incorrect.")
            raise InvalidPasswordError("Current password is incorrect.")

        if password_change.new_password != password_change.new_password_confirmation:
            logging.error("New password and confirmation do not match.")
            raise PasswordMismatchError("New password and confirmation do not match.")

        user.hashed_password = get_password_hash(password_change.new_password)
        db.commit()
        return None
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        raise
