from collections.abc import Callable

from schemas import MessageDict


def append_generate_code(conversation: list[MessageDict]) -> list[MessageDict]:
    """
    Appends a message to the conversation list that requests to generate code for all the files in the project structure.

    Args:
        conversation (list[MessageDict]): A list of messages exchanged between users.

    Returns:
        list[MessageDict]: The updated conversation list with the appended message.
    """

    conversation.append(
        {
            "role": "user",
            "content": """
                    Generate code for all the files in the project structure.\n
                    Please use 'File: {Project Name}/{path}/{filename}' as a tag for the file before the code block. And 'Done: {Project Name}/{path}/{filename}' as a tag for the file after the code block.\n
                    When finished, please type '---Finished---' to end the chat.
                    """.strip(),
        },
    )
    return conversation


def quit_chat(conversation: list[MessageDict]) -> list[MessageDict]:
    exit("User exited the chat.")


chat_commands: dict[str, Callable[[list[MessageDict]], list[MessageDict]]] = {
    "create_code": append_generate_code,
    "exit": quit_chat,
    "exit()": quit_chat,
    "quit": quit_chat,
    "quit()": quit_chat,
}
