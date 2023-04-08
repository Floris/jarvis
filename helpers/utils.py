import os

from prompts.prompts import PROMPT_NAME


def remove_code_block(s: str) -> str:
    """
    Removes the code block from the prompt.

    Args:
        s (str): The prompt.

    Returns:
        str: The prompt with the code block removed.
    """
    return "" if "```" in s else s


def parse_str(s: str, replacement: str) -> str:
    return s.replace(replacement, "")


def remove_whitespace(s):
    """
    Removes all whitespace characters from a string.

    Args:
        s (str): The input string.

    Returns:
        str: The string with all whitespace removed.
    """
    return "".join(s.split())


def save_code_to_file(code: str, file_path: str, file: str) -> None:
    """
    Save the generated code into the specified file.

    Args:
        code (str): The generated code.
        file_path (str): The path to the file where the code should be saved.

    Returns:
        None
    """

    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, PROMPT_NAME)
    )
    print("base_path ===> ", base_path)  # TODO: remove later

    def from_base_path_create_folder(folder_name):
        folder = os.path.join(base_path, folder_name)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    from_base_path_create_folder(file_path)

    file_path = os.path.join(base_path, file_path, file)

    print(f"Saving code to file: {file_path}")  # TODO: remove later

    with open(file_path, "w") as f:
        f.write(code)

    print(f"saved file: {file_path}")
