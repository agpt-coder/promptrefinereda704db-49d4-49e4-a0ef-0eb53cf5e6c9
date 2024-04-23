import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserDetailsResponse(BaseModel):
    """
    Response model containing detailed information about the user, excluding sensitive fields such as a password.
    """

    id: int
    email: str
    role: prisma.enums.Role


async def getUser(id: str) -> UserDetailsResponse:
    """
    Retrieves details of a specific user based on the user id. Returns user information including email and role, excluding sensitive data like passwords. This supports user account management functions.

    Args:
        id (str): The unique identifier of the user, used to fetch user details.

    Returns:
        UserDetailsResponse: Response model containing detailed information about the user, excluding sensitive fields such as a password.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": int(id)})
    if user is None:
        raise ValueError(f"No user found with id {id}")
    return UserDetailsResponse(id=user.id, email=user.email, role=user.role.name)
