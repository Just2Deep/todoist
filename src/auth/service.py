from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import uuid4
from fastapi import Depends
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from src.entities.user import User
from . import model
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..exceptions import AuthenticationError
import logging

import os

SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with your actual secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return bcrypt_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    """
    Authenticate a user by email and password.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        logging.error(f"Authentication failed for user: {email}")
        return False
    return user


def create_access_token(email: str, user_id: str, expires_delta: timedelta) -> str:
    """
    Create a JWT access token.
    """
    to_encode = {
        "sub": email,
        "id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> model.TokenData:
    """
    Verify a JWT token and return the token data.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        return model.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.error(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def register_user(db: Session, user_data: model.RegisterUserRequest) -> User:
    """
    Register a new user in the database.
    """
    try:
        new_user = User(
            id=uuid4(),
            email=user_data.email,
            username=user_data.username,
            password=get_password_hash(user_data.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logging.error(f"User registration failed: {str(e)}")
        db.rollback()
        raise


def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
) -> model.TokenData:
    """
    Get the current authenticated user from the token.
    """
    return verify_token(token)


CurrentUser = Annotated[User, Depends(get_current_user)]


def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_bearer)], db: Session
) -> model.Token:
    """
    Authenticate a user and return an access token.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logging.error("Invalid credentials provided.")
        raise AuthenticationError()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        email=user.email, user_id=str(user.id), expires_delta=access_token_expires
    )
    return model.Token(access_token=access_token, token_type="bearer")
