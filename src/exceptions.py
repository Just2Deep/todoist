class AuthenticationError(Exception):
    """Raised when there is an authentication error."""

    pass


class AuthorizationError(Exception):
    """Raised when there is an authorization error."""

    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found."""

    def __init__(self, message: str = "User not found."):
        super().__init__(message)
        self.message = message


class InvalidPasswordError(Exception):
    """Raised when the provided password is invalid."""

    def __init__(self, message: str = "Invalid password."):
        super().__init__(message)
        self.message = message


class PasswordMismatchError(Exception):
    """Raised when the new password and confirmation do not match."""

    def __init__(self, message: str = "New password and confirmation do not match."):
        super().__init__(message)
        self.message = message
