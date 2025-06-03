from fastapi import HTTPException


class AuthenticationError(HTTPException):
    """Raised when there is an authentication error."""

    def __init__(self, message: str = "Authentication failed."):
        super().__init__(status_code=401, detail=message)


class AuthorizationError(HTTPException):
    """Raised when there is an authorization error."""

    def __init__(self, message: str = "Authorization failed."):
        super().__init__(status_code=403, detail=message)


class UserNotFoundError(HTTPException):
    """Raised when a user is not found."""

    def __init__(self, message: str = "User not found."):
        super().__init__(status_code=404, detail=message)


class InvalidPasswordError(HTTPException):
    """Raised when the provided password is invalid."""

    def __init__(self, message: str = "Invalid password."):
        super().__init__(status_code=401, detail=message)


class PasswordMismatchError(HTTPException):
    """Raised when the new password and confirmation do not match."""

    def __init__(self, message: str = "New password and confirmation do not match."):
        super().__init__(status_code=400, detail=message)


class TodoNotFoundError(HTTPException):
    """Raised when a todo item is not found."""

    def __init__(self, message: str = "Todo item not found."):
        super().__init__(status_code=404, detail=message)


class TodoCreationError(HTTPException):
    """Raised when there is an error creating a todo item."""

    def __init__(self, message: str = "Error creating todo item."):
        super().__init__(status_code=500, detail=message)
