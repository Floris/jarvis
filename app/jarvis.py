import openai
from chat import generate_chat, handle_incoming_message
from helpers.processor import process_input
from questions import QuestionApp, use_prompt_from_file
from schemas import MessageDict

from settings import settings

openai.api_key = settings.api_key


def main() -> None:
    """
    Asks a series of questions to gather information, generates a prompt based on the answers.

    Commands:
        - create_code: Generates code for all the files in the project structure.
        - exit: Exits the chat.
    """

    # Start
    initial_prompt = use_prompt_from_file()

    if initial_prompt is None:
        app = QuestionApp()
        app.ask_questions()

        # Generate the prompt based on the answers
        initial_prompt = app.generate_prompt()

    conversation: list[MessageDict] = [
        {
            "role": "system",
            "content": """
            You are a world class software developer.
            You will design project structure based on the information provided.
            """.strip(),
        },
        {
            "role": "user",
            "content": initial_prompt.strip(),
        },
    ]

    while True:
        print("processing...")

        conversation, _ = generate_chat(1, temperature=0.8)
        incoming_message = conversation[-1]["content"].strip()

        handle_incoming_message(incoming_message)

        # Get the user input
        answer = input(f"{incoming_message}: ")

        conversation = process_input(answer, conversation)


if __name__ == "__main__":
    main()
