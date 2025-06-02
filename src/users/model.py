from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_confirmation: str
