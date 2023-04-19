from agent.coding_assistant import CodingAssistant
from agent.manager import delete_agent, list_agents, message_agent, start_agent
from exceptions import ShutDown
from helpers.file_helpers import append_to_file, read_file, write_to_file


def handle_command(name: str, args: dict) -> str:
    """
    Handle the execution of a command based on its name and arguments.

    Args:
        name (str): The name of the command.
        args (dict): A dictionary of arguments for the command.

    Returns:
        Any: The result of the command execution.

    Raises:
        ShutDown: If the command is 'shutdown', raise the ShutDown exception.
    """
    if name == "shutdown":
        raise ShutDown("Shutdown command received.")

    elif name == "start_coding_assistant":
        return CodingAssistant(
            name=args["name"], project_structure_file_name=args["file_name"]
        ).start()

    elif name == "start_agent":
        return start_agent(args["name"], task=args["task"], prompt=args["prompt"])

    elif name == "message_agent":
        return message_agent(args["key"], args["message"])

    elif name == "list_agents":
        return list_agents()

    elif name == "delete_agent":
        return delete_agent(args["key"])

    elif name in ["append_to_file", "update_file"]:
        append_to_file(
            filename=args["file"],
            text=args["text"],
        )
        response = f'Updated file: {args["file"]}'

    elif name in [
        "write_to_file",
        "create_file",
    ]:
        write_to_file(
            filename=args["file"],
            text=args["text"],
        )
        response = f'Saved data to file: {args["file"]}'

    elif name == "read_file":
        response = read_file(filename=args["file"])

    elif name == "do_nothing":
        return "No action performed."

    else:
        response = "Command not recognized."

    return response
