import base64
import hashlib
import os

import prisma
import prisma.models
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Provides a session token after successful authentication. The token should be used in subsequent requests to authenticate the user's session.
    """

    token: str


async def userLogin(email: str, password: str) -> UserLoginResponse:
    """
    Authenticates user's credentials and generates a session token. Takes in an email and password, returns a token which is used to handle sessions and validate future requests. Critical for user security and session management.

    Args:
        email (str): The email address associated with the user's account.
        password (str): The password for the user account, which should be transmitted securely.

    Returns:
        UserLoginResponse: Provides a session token after successful authentication. The token should be used in subsequent requests to authenticate the user's session.

    Raises:
        ValueError: If the email or password does not match any user in the database.
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = await prisma.models.User.prisma().find_unique(
        where={"email": email, "password": hashed_password}
    )
    if user is None:
        raise ValueError("Invalid email/password combination.")
    token_bytes = os.urandom(48)
    token = base64.urlsafe_b64encode(token_bytes).decode("utf-8")
    return UserLoginResponse(token=token)
