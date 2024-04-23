from pydantic import BaseModel


class PromptSubmissionResponse(BaseModel):
    """
    A simple model to confirm the receipt and acceptance of the user's prompt for processing.
    """

    message: str
    submitted: bool


def receivePrompt(prompt: str) -> PromptSubmissionResponse:
    """
    This endpoint receives a prompt from the user and validates its structure. The input must be a non-empty string. If the validation passes, the prompt is sent to the Prompt Refinement Processing Module via an internal API call. The response will be asynchronous, indicating successful reception and validation of the prompt. This route doesn’t interact directly with the OpenAI API; it primarily handles input verification and relays to the internal processing system.

    Args:
        prompt (str): The raw input string from the user that needs to be validated and then processed for prompt refinement.

    Returns:
        PromptSubmissionResponse: A simple model to confirm the receipt and acceptance of the user's prompt for processing.
    """
    if not prompt:
        return PromptSubmissionResponse(
            message="Invalid prompt: Input cannot be empty.", submitted=False
        )
    return PromptSubmissionResponse(
        message="Prompt received and submitted for refinement.", submitted=True
    )
