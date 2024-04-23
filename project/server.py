import logging
from contextlib import asynccontextmanager

import prisma
import prisma.enums
import project.createUser_service
import project.deleteUser_service
import project.getUser_service
import project.receivePrompt_service
import project.refinePrompt_service
import project.updateUser_service
import project.userLogin_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="PromptRefiner",
    lifespan=lifespan,
    description='Create a single API endpoint that takes in a string LLM prompt, and returns a refined version which has been improved by GPT4. To "refine" the prompt, use the OpenAI Python package to interface with their AI, and use the GPT4 model. Use this system message: "You are a prompt refiner. Use advanced prompt engineering techniques to refine the user\'s prompt." and send the user\'s prompt as the user message.',
)


@app.post(
    "/api/v1/prompts",
    response_model=project.receivePrompt_service.PromptSubmissionResponse,
)
async def api_post_receivePrompt(
    prompt: str,
) -> project.receivePrompt_service.PromptSubmissionResponse | Response:
    """
    This endpoint receives a prompt from the user and validates its structure. The input must be a non-empty string. If the validation passes, the prompt is sent to the Prompt Refinement Processing Module via an internal API call. The response will be asynchronous, indicating successful reception and validation of the prompt. This route doesn’t interact directly with the OpenAI API; it primarily handles input verification and relays to the internal processing system.
    """
    try:
        res = project.receivePrompt_service.receivePrompt(prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/:id", response_model=project.updateUser_service.UpdateUserDetailsResponse
)
async def api_put_updateUser(
    id: int, email: str, role: prisma.enums.Role
) -> project.updateUser_service.UpdateUserDetailsResponse | Response:
    """
    Updates user details for an existing user, except for the password. Accepts updatable user details as input and returns a success message upon successful update. Utilized for user account updates by admins.
    """
    try:
        res = await project.updateUser_service.updateUser(id, email, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/refine-prompt", response_model=project.refinePrompt_service.RefinedPromptResponse
)
async def api_post_refinePrompt(
    original_prompt: str, user_id: int
) -> project.refinePrompt_service.RefinedPromptResponse | Response:
    """
    This endpoint accepts a POST request containing a user's prompt in the form of a simple string. It utilizes the OpenAI Python package to interact with the GPT-4 AI model. The system sets the context with an advanced prompt engineering technique stating 'You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.' Then, the user's original prompt is processed by the AI, and a refined version of the prompt is returned. The process ensures high-quality output suitable for optimized interactions with AI models.
    """
    try:
        res = await project.refinePrompt_service.refinePrompt(original_prompt, user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    email: str, password: str, role: prisma.enums.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    Creates a new user account. Accepts user details such as email, password, and role. Returns the user id and a message indicating successful creation. This endpoint uses hashing algorithms to securely store user passwords.
    """
    try:
        res = await project.createUser_service.createUser(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete("/users/:id", response_model=project.deleteUser_service.DeleteUserResponse)
async def api_delete_deleteUser(
    id: int,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a specific user from the system based on user id. Used by admins to manage user access and ensure data privacy and regulatory compliance. Returns a confirmation message upon successful deletion.
    """
    try:
        res = await project.deleteUser_service.deleteUser(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users/login", response_model=project.userLogin_service.UserLoginResponse)
async def api_post_userLogin(
    email: str, password: str
) -> project.userLogin_service.UserLoginResponse | Response:
    """
    Authenticates user's credentials and generates a session token. Takes in an email and password, returns a token which is used to handle sessions and validate future requests. Critical for user security and session management.
    """
    try:
        res = await project.userLogin_service.userLogin(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/:id", response_model=project.getUser_service.UserDetailsResponse)
async def api_get_getUser(
    id: str,
) -> project.getUser_service.UserDetailsResponse | Response:
    """
    Retrieves details of a specific user based on the user id. Returns user information including email and role, excluding sensitive data like passwords. This supports user account management functions.
    """
    try:
        res = await project.getUser_service.getUser(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
