import os
import os.path
from collections.abc import Generator

working_directory = "generated"

# Create the directory if it doesn't exist
if not os.path.exists(working_directory):
    os.makedirs(working_directory)


def safe_join(base: str, *paths: str) -> str:
    """Join one or more path components intelligently."""
    new_path = os.path.join(base, *paths)
    norm_new_path = os.path.normpath(new_path)

    if os.path.commonprefix([base, norm_new_path]) != base:
        raise ValueError("Attempted to access outside of working directory.")

    return norm_new_path


def split_file(
    content: str, max_length: int = 4000, overlap: int = 0
) -> Generator[str, None, None]:
    """
    Split text into chunks of a specified maximum length with a specified overlap
    between chunks.
    :param text: The input text to be split into chunks
    :param max_length: The maximum length of each chunk,
        default is 4000 (about 1k token)
    :param overlap: The number of overlapping characters between chunks,
        default is no overlap
    :return: A generator yielding chunks of text
    """
    start = 0
    content_length = len(content)

    while start < content_length:
        end = start + max_length
        yield content[
            start : end + overlap  # noqa: E203
        ] if end + overlap < content_length else content[start:content_length]
        start += max_length - overlap


def read_file(filename: str) -> str:
    """Read a file and return the contents"""
    try:
        filepath = safe_join(working_directory, filename)
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error: {str(e)}"


def write_to_file(filename: str, text: str) -> str:
    """Write text to a file"""
    try:
        filepath = safe_join(working_directory, filename)
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        return "File written to successfully."
    except Exception as e:
        return "Error: " + str(e)


def append_to_file(filename: str, text: str) -> str:
    """Append text to a file"""
    try:
        filepath = safe_join(working_directory, filename)
        with open(filepath, "a") as f:
            f.write(text)
        return "Text appended successfully."
    except Exception as e:
        return "Error: " + str(e)


def delete_file(filename: str) -> str:
    """Delete a file"""
    try:
        filepath = safe_join(working_directory, filename)
        os.remove(filepath)
        return "File deleted successfully."
    except Exception as e:
        return "Error: " + str(e)


def search_files(directory: str) -> list[str]:
    found_files = []

    if directory == "" or directory == "/":
        search_directory = working_directory
    else:
        search_directory = safe_join(working_directory, directory)

    for root, _, files in os.walk(search_directory):
        for file in files:
            if file.startswith("."):
                continue
            relative_path = os.path.relpath(os.path.join(root, file), working_directory)
            found_files.append(relative_path)

    return found_files


def save_code_to_file(code: str, file_path: str, file: str) -> None:
    """
    Save the generated code into the specified file. Always saves to the generated folder.

    Args:
        code (str): The generated code.
        file_path (str): The path to the file where the code should be saved.
        file (str): The name of the file where the code should be saved.

    Returns:
        None
    """

    # This sets the base path to the root of the project.
    base_path = f"{os.path.abspath(os.path.join(os.getcwd()))}/generated"

    def from_base_path_create_folder(folder_name: str) -> str:
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
