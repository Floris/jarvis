import os


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
        file (str): The name of the file where the code should be saved.

    Returns:
        None
    """

    # This sets the base path to the root of the project.
    base_path = f"{os.path.abspath(os.path.join(os.getcwd()))}/generated"

    def from_base_path_create_folder(folder_name):
        folder = os.path.join(base_path, folder_name)
        if not os.path.exists(folder):
            print(f"Creating folder: {folder}")
            os.makedirs(folder)
        return folder

    # create path from file_path
    from_base_path_create_folder(file_path)

    file_path = os.path.join(base_path, file_path, file)

    print(f"Saving code to file: {file_path}")  # TODO: remove later

    # append code to file, using append incase the file already exists
    with open(file_path, "a") as f:
        f.write(code)

    print(f"saved file: {file_path}")
