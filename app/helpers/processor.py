import re

from helpers.commands import chat_commands
from helpers.utils import remove_code_block, remove_whitespace
from schemas import MessageDict

file_pattern = re.compile(r".*File:")


def parse_response(response: str) -> list[tuple[str, str, str]]:
    """
    Parse a string that contains information about a project's file structure and contents.

    Args:
        response (str): The response string to parse.

    Returns:
        A list of tuples containing folder path, file name, and file code.
    """
    file_code_pairs = []
    current_folder = ""
    current_file = ""
    current_code: list[str] = []
    parsing_code = False

    for line in response.splitlines():
        if "The project structure should look like this:" in line:
            continue

        elif "File:" in line:
            if parsing_code:
                # Add the previous file's code to the file_code_pairs list
                file_code_pairs.append(
                    (current_folder, current_file, "\n".join(current_code))
                )
                current_code = []

            parsing_code = True
            file_path = remove_whitespace(file_pattern.sub("", line))

            current_folder, current_file = (
                file_path.rsplit("/", 1) if "/" in file_path else ("", file_path)
            )

        elif parsing_code and line.strip():
            if "Done:" in line:
                # Add the previous file's code to the file_code_pairs list
                file_code_pairs.append(
                    (current_folder, current_file, "\n".join(current_code))
                )
                current_code = []
                parsing_code = False
            else:
                current_code.append(remove_code_block(line))

    # Add the last file's code to the file_code_pairs list
    if parsing_code:
        file_code_pairs.append((current_folder, current_file, "\n".join(current_code)))

    return file_code_pairs


def process_input(answer: str, conversation: list[MessageDict]) -> list[MessageDict]:
    """
    Processes the user's input.

    Args:
        answer str: The user's input.
        conversation list[MessageDict]: The conversation so far.

    Returns:
        list[MessageDict]: The updated conversation.
    """

    if answer in {"exit", "quit", "stop", "done"}:
        exit(code="User exited the chat.")

    # Append the command's response to the conversation list
    if answer in chat_commands.keys():
        conversation = chat_commands[answer](conversation)
        return conversation

    # Append the user's answer to the conversation list
    conversation.append(
        {
            "role": "user",
            "content": answer,
        },
    )

    return conversation
