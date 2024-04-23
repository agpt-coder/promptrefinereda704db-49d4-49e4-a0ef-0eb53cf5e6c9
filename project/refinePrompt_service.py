import openai
import prisma
import prisma.models
from pydantic import BaseModel


class RefinedPromptResponse(BaseModel):
    """
    Outputs the refined version of the prompt along with the original for comparison and alignment.
    """

    original_prompt: str
    refined_prompt: str


async def refinePrompt(original_prompt: str, user_id: int) -> RefinedPromptResponse:
    """
    Refines a user's input prompt using the OpenAI GPT-4 model, under advanced prompt engineering techniques.

    This function first checks for the existence of the user in the database. It then creates an enhanced system
    prompt that incorporates the user's original prompt and uses the OpenAI GPT-4 model to generate a refined prompt.
    The function will also record the original and refined prompts in the database associated with the respective user.

    Args:
        original_prompt (str): The original user input prompt that needs to be refined.
        user_id (int): The ID of the user sending the prompt. It's crucial for access control and tracking prompt ownership.

    Returns:
        RefinedPromptResponse: Outputs the refined version of the prompt along with the original for comparison and alignment.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        raise ValueError("User with given ID not found")
    system_prompt = f"You are a prompt refiner. Use advanced prompt engineering techniques to refine this prompt: {original_prompt}"
    response = openai.Completion.create(
        model="gpt-4", prompt=system_prompt, max_tokens=150
    )
    refined_prompt = response.choices[
        0
    ].text.strip()  # TODO(autogpt): Cannot access attribute "choices" for class "Generator[Unknown | list[Unknown] | dict[Unknown, Unknown], None, None]"
    #     Attribute "choices" is unknown. reportAttributeAccessIssue
    new_prompt = await prisma.models.Prompt.prisma().create(
        data={"content": original_prompt, "refined": refined_prompt, "userId": user_id}
    )
    return RefinedPromptResponse(
        original_prompt=original_prompt, refined_prompt=refined_prompt
    )
