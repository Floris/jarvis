from typing import Literal

import openai
from helpers.processor import parse_response
from helpers.utils import remove_whitespace, save_code_to_file
from questions import QuestionApp
from schemas import ApiResponse, Message

from settings import settings

openai.api_key = settings.api_key


def generate_chat(
    conversation: list[Message],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
    stop: str | list[str] | None = None,
) -> tuple[list[Message], Literal["length", "stop", "eos"]]:
    """
    Generate a chat response from the OpenAI API.

    Args:
        conversation (List[Message]): A list of Message dictionaries representing the conversation so far.
        model (str, optional): The OpenAI model to use for the chat. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): Controls randomness in the generated response. Defaults to 0.5.
        stop (Union[str, List[str], None], optional): Token(s) that indicate the end of the generated response. Defaults to None.

    Returns:
        tuple[List[Message], Literal["length", "stop", "eos"]]: Updated conversation list and the reason the conversation finished.
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
    print(
        "API response.choices[0].message['role'] ===> ",
        response.choices[0].message["role"],
    )
    print(
        "API response.choices[0].message['content'] ===> ",
        response.choices[0].message["content"],
    )

    conversation.append(
        Message(
            role=response.choices[0].message["role"],
            content=response.choices[0].message["content"],
        )
    )

    return conversation, response.choices[0].finish_reason


def main():
    app = QuestionApp()
    app.ask_questions()

    prompt = app.generate_prompt()
    print("PROMPT: ", prompt)

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
            "content": prompt,
        },
    ]

    # Allow max 3 api calls
    for index in range(3):
        print(f"GENERATING CHAT --- index:{index}")
        conversation, finish_reason = generate_chat(conversation)

        if finish_reason == "stop":
            break

    file_code_pairs: list[tuple[str, str, str]] = []
    for message in conversation:
        # we only care about the assistant's responses
        if message["role"] != "assistant":
            continue
        file_code_pairs.extend(parse_response(message["content"].strip()))

    for current_folder, current_file, code in file_code_pairs:
        save_code_to_file(
            code,
            remove_whitespace(current_folder),
            remove_whitespace(current_file),
        )


if __name__ == "__main__":
    main()
