import openai
from chat import generate_chat
from helpers.processor import parse_response
from helpers.utils import remove_whitespace, save_code_to_file
from questions import QuestionApp
from schemas import MessageDict

from settings import settings

openai.api_key = settings.api_key


def main():
    app = QuestionApp()
    app.ask_questions()

    prompt = app.generate_prompt()
    print("PROMPT: ", prompt)

    conversation: list[MessageDict] = [
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
