from typing import Literal, TypedDict

import openai
from helpers.processor import parse_response
from helpers.utils import remove_whitespace, save_code_to_file
from prompts.prompts import PROMPT
from pydantic import BaseModel

from settings import settings

openai.api_key = settings.api_key


class Message(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Literal["length", "stop", "eos"]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ApiResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: list[Choice]


def generate_chat(
    conversation: list[Message],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
    stop: str | list[str] | None = None,
) -> tuple[list[Message], Literal["length", "stop", "eos"]]:
    """
    Generate a chat response from the OpenAI API.
    """

    response = ApiResponse.parse_obj(
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
    print("API response.choices[0].message ===> ", response.choices[0].message)

    conversation.append(
        Message(
            role=response.choices[0].message["role"],
            content=response.choices[0].message["content"],
        )
    )

    return conversation, response.choices[0].finish_reason


def main():
    conversation: list[Message] = [
        {
            "role": "system",
            "content": """
            You are a coding assistant that generates code + project structure based on the Project Structure defined.
            You utilize best practices and are a great resource for developers.
            """.strip(),
        },
        {
            "role": "user",
            "content": PROMPT,
        },
    ]

    finish_reason = None
    index = 0
    while finish_reason != "stop":
        print(f"GENERATING CHAT --- index:{index}")

        if index >= 3:
            raise Exception("Too many iterations")

        index += 1
        conversation, finish_reason = generate_chat(conversation)

    file_code_pairs: list[tuple[str, str, str]] = []
    for message in conversation:
        # only parse assistant messages
        if message["role"] != "assistant":
            continue
        file_code_pairs.extend(parse_response(message["content"].strip()))

    print(f"Parsed file code pairs: {file_code_pairs}")

    for current_folder, current_file, code in file_code_pairs:
        save_code_to_file(
            code,
            remove_whitespace(current_folder),
            remove_whitespace(current_file),
        )


if __name__ == "__main__":
    main()
