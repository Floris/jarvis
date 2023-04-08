import openai

import settings
from helpers.processor import parse_response
from helpers.utils import remove_whitespace, save_code_to_file
from prompts.prompts import PROMPT

openai.api_key = settings.api_key


def generate_chat(
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 2200,
    n: int = 1,
    stop: str | list[str] | None = None,
    temperature: float = 0.5,
):
    messages = [
        {
            "role": "system",
            "content": "You are a legendary coding assistant that generates code + project structure when needed.",  # noqa E501
        },
        {
            "role": "user",
            "content": PROMPT,
        },
    ]

    # Call the OpenAI API to get the chat response
    response = openai.ChatCompletion.create(
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
        model=model,
        messages=messages,
    )

    print("API Response:")  # TODO: remove later
    print(response)

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    response = generate_chat()
    print(f"Response: {response}")  # TODO: remove later

    file_code_pairs = parse_response(response)
    print(f"Parsed file code pairs: {file_code_pairs}")  # TODO: remove later

    for current_folder, current_file, code in file_code_pairs:
        save_code_to_file(
            code,
            remove_whitespace(current_folder),
            remove_whitespace(current_file),
        )
