import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpdateUserDetailsResponse(BaseModel):
    """
    Confirmation that the user details have been updated successfully.
    """

    success: bool
    message: str


async def updateUser(
    id: int, email: str, role: prisma.enums.Role
) -> UpdateUserDetailsResponse:
    """
    Updates user details for an existing user, except for the password. Accepts updatable user details as input
    and returns a success message upon successful update. Utilized for user account updates by admins.

    Args:
        id (int): Unique identifier of the user to be updated.
        email (str): Updated email address of the user.
        role (prisma.enums.Role): Updated role of the user within the system. Allowed values are 'Admin', 'User', 'SystemOperator'.

    Returns:
        UpdateUserDetailsResponse: Confirmation that the user details have been updated successfully.
    """
    try:
        if not isinstance(role, prisma.enums.Role):
            return UpdateUserDetailsResponse(
                success=False, message="Invalid role specified."
            )
        user = await prisma.models.User.prisma().update(
            where={"id": id}, data={"email": email, "role": role.name}
        )
        return UpdateUserDetailsResponse(
            success=True, message="User details have been successfully updated."
        )
    except Exception as error:
        return UpdateUserDetailsResponse(
            success=False, message=f"Failed to update user: {str(error)}"
        )
