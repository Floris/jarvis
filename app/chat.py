from typing import Literal

import openai
from helpers.processor import parse_response
from helpers.utils import remove_whitespace, save_code_to_file
from schemas import ApiResponseSchema, MessageDict

from settings import settings

openai.api_key = settings.api_key


def generate_chat(
    conversation: list[MessageDict],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
    stop: str | list[str] | None = None,
) -> tuple[list[MessageDict], Literal["length", "stop", "eos"]]:
    """
    Generate a chat response from the OpenAI API. Appends the response to the conversation list.

    Args:
        conversation (List[MessageDict]): A list of Message dictionaries representing the conversation so far.
        model (str, optional): The OpenAI model to use for the chat. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): Controls randomness in the generated response. Defaults to 0.5.
        stop (Union[str, List[str], None], optional): Token(s) that indicate the end of the generated response. Defaults to None.

    Returns:
        tuple[List[MessageDict], Literal["length", "stop", "eos"]]: Updated conversation list and the reason the conversation finished.
    """

    response = ApiResponseSchema.parse_obj(
        openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            temperature=temperature,
            stop=stop,
        )
    )

    print("API response.usage ===> ", response.usage)

    conversation.append(
        MessageDict(
            role=response.choices[0].message["role"],
            content=response.choices[0].message["content"],
        )
    )

    return conversation, response.choices[0].finish_reason


def handle_incoming_message(incoming_message: str) -> None:
    """
    Handles the incoming message from the OpenAI API.

    Args:
        incoming_message str: The incoming message from the OpenAI API.

    Returns:
        None
    """

    # Parse latest chat response to get the code
    file_code_pairs = parse_response(incoming_message)

    # Save the generated code
    for current_folder, current_file, code in file_code_pairs:
        save_code_to_file(
            code,
            remove_whitespace(current_folder),
            remove_whitespace(current_file),
        )
