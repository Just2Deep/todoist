from uuid import UUID
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str | None = None

    def get_uuid(self) -> UUID | None:
        """
        Returns the user ID as a UUID if it is not None.
        """
        if self.user_id is None:
            return None
        return UUID(self.user_id)
