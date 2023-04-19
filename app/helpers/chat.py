import logging
from typing import Literal

import openai
from schemas import ApiResponseSchema, MessageDict

logger = logging.getLogger()


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

    logger.debug("=====================================")
    logger.debug("Prompt:")
    logger.debug(conversation[-1]["content"])
    logger.debug("=====================================")

    response = ApiResponseSchema.parse_obj(
        openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            temperature=temperature,
            stop=stop,
        )
    )

    logger.info(("API response.usage ===> ", response.usage))
    logger.debug(("API response content ===> ", response.choices[0].message["content"]))

    conversation.append(
        MessageDict(
            role=response.choices[0].message["role"],
            content=response.choices[0].message["content"],
        )
    )

    return conversation, response.choices[0].finish_reason


def create_conversation_message(
    role: Literal["system", "user"], content: str
) -> MessageDict:
    """
    Create a conversation message dictionary.

    Args:
        role (Literal["system", "user"]): The role of the message sender.
        content (str): The content of the message.

    Returns:
        MessageDict: The created message dictionary.
    """
    return {"role": role, "content": content}
