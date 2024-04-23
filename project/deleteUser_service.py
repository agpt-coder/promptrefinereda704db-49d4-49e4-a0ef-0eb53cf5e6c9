import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model indicating the outcome of the delete operation. It provides a message confirming the successful deletion of the user.
    """

    message: str


async def deleteUser(id: int) -> DeleteUserResponse:
    """
    Deletes a specific user from the system based on user id. Used by admins to manage user access and ensure data privacy and regulatory compliance. Returns a confirmation message upon successful deletion.

    Args:
        id (int): The unique identifier of the user to be deleted. It is provided as a path parameter.

    Returns:
        DeleteUserResponse: Response model indicating the outcome of the delete operation. It provides a message confirming the successful deletion of the user.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": id})
    if not user:
        return DeleteUserResponse(
            message=f"No user found with ID {id}. No action taken."
        )
    await prisma.models.User.prisma().delete(where={"id": id})
    return DeleteUserResponse(
        message=f"User with ID {id} has been successfully deleted."
    )
