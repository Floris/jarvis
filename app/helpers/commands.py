from collections.abc import Callable

from schemas import MessageDict


def append_generate_code(conversation: list[MessageDict]) -> list[MessageDict]:
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


chat_commands: dict[str, Callable] = {
    "create_code": append_generate_code,
}
