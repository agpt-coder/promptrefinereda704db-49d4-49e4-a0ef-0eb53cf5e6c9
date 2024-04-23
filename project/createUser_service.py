from enum import Enum

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    This model describes the response returned after creating a user, including the user ID and a success message.
    """

    user_id: int
    message: str


class Role(Enum):
    Admin: str = "Admin"
    User: str = "User"
    SystemOperator: str = "SystemOperator"


async def createUser(email: str, password: str, role: Role) -> CreateUserResponse:
    """
    Creates a new user account. Accepts user details such as email, password, and role.
    Returns the user id and a message indicating successful creation.
    This endpoint uses hashing algorithms to securely store user passwords.

    Args:
        email (str): The email address of the new user, must be unique.
        password (str): The password for the new user account, which will be hashed in storage.
        role (Role): The role of the new user which determines their access control levels.

    Returns:
        CreateUserResponse: This model describes the response returned after creating
                            a user, including the user ID and a success message.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    created_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password.decode(), "role": role}
    )
    response = CreateUserResponse(
        user_id=created_user.id, message="User created successfully."
    )
    return response
