def remove_code_block(s: str) -> str:
    """
    Removes the code block from the prompt.

    Args:
        s (str): The prompt.

    Returns:
        str: The prompt with the code block removed.
    """
    return "" if "```" in s else s


def remove_whitespace(s):
    """
    Removes all whitespace characters from a string.

    Args:
        s (str): The input string.

    Returns:
        str: The string with all whitespace removed.
    """
    return "".join(s.split())


def is_int(value: str) -> bool:
    """Check if the value is a valid integer
    Args:
        value (str): The value to check
    Returns:
        bool: True if the value is a valid integer, False otherwise
    """
    try:
        int(value)
        return True
    except ValueError:
        return False
