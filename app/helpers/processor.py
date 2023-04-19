import re

from helpers.utils import remove_code_block, remove_whitespace

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

    def add_current_code():
        file_code_pairs.append((current_folder, current_file, "\n".join(current_code)))
        current_code.clear()

    for line in response.splitlines():
        if "File:" in line:
            if parsing_code:
                add_current_code()

            parsing_code = True
            file_path = remove_whitespace(file_pattern.sub("", line))

            current_folder, current_file = (
                file_path.rsplit("/", 1) if "/" in file_path else ("", file_path)
            )

        elif parsing_code and line.strip():
            if "Done:" not in line:
                current_code.append(remove_code_block(line))
                continue

            add_current_code()
            parsing_code = False

    if parsing_code:
        add_current_code()

    return file_code_pairs
