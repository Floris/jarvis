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

    for line in response.splitlines():
        if "The project structure should look like this:" in line:
            continue

        elif "File:" in line:
            line = remove_whitespace(line)
            print("line ===> ", line)  # TODO: remove later

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
