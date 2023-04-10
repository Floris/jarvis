from typing import Literal

import openai
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
    Generate a chat response from the OpenAI API.

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

    print("API response.object ===> ", response.object)
    print("API response.usage ===> ", response.usage)
    print(
        "API response.choices[0].finish_reason ===> ", response.choices[0].finish_reason
    )
    print(
        "API response.choices[0].message['role'] ===> ",
        response.choices[0].message["role"],
    )
    print(
        "API response.choices[0].message['content'] ===> ",
        response.choices[0].message["content"],
    )

    conversation.append(
        MessageDict(
            role=response.choices[0].message["role"],
            content=response.choices[0].message["content"],
        )
    )

    return conversation, response.choices[0].finish_reason
