import logging

from helpers.chat import create_conversation_message, generate_chat
from helpers.file_helpers import read_file, save_code_to_file
from helpers.processor import parse_response
from helpers.utils import remove_whitespace
from schemas import MessageDict

logger = logging.getLogger()


# TODO: Integrate this into the Agent class
class CodingAssistant:
    """
    Assistant that can only generate code for a project structure.
    """

    def __init__(self, name: str, project_structure_file_name: str) -> None:
        """
        Args:
            name (str): The name of the Coding Agent.
            project_structure_file_name (str): The name of the file that contains the project information/ structure.
        """
        self.name = name
        self.project_structure_file_name = project_structure_file_name

    def construct_prompt(self) -> str:
        """
        Constructs the prompt for the AI to generate code for the project structure.
        """
        prompt = read_file(filename=self.project_structure_file_name)
        prompt += "\n\n Generate code for all the files and information in the project structure.\n"
        prompt += "\n Use your imagination, do not deliver empty functions.\n"
        prompt += "Please use 'File: {Project Name}/{path}/{filename}' as a tag for the file before the code block. And 'Done: {Project Name}/{path}/{filename}' as a tag for the file after the code block.\n"
        prompt += "When finished, please type '---Finished---' to end the chat."
        return prompt

    def start(self) -> str:
        logger.info("=====================================")
        logger.info(f"Starting agent {self.name}")
        logger.info(f"Project structure file name: {self.project_structure_file_name}")
        logger.info("=====================================")

        prompt = self.construct_prompt()

        conversation: list[MessageDict] = [
            create_conversation_message(
                "system",
                "You are a Legendary Software Engineer, you know everything there is to know about software engineering. When creating the code you always finish what you start. You cannot ask for help. ",
            ),
            create_conversation_message("user", prompt),
        ]

        conversation, _ = generate_chat(conversation, temperature=0.0)
        incoming_message = conversation[-1]["content"].strip()

        # Parse latest chat response to get the code
        file_code_pairs = parse_response(incoming_message)

        actions_list = []
        # Save the generated code
        for current_folder, current_file, code in file_code_pairs:
            actions_list.append(f"{current_folder}/{current_file}")
            save_code_to_file(
                code,
                remove_whitespace(current_folder),
                remove_whitespace(current_file),
            )

        response = f"Agent {self.name} has finished coding. Response: created code for file(s): {', '.join(actions_list)}"
        logger.info("=====================================")
        logger.info(f"Shutting down agent {self.name}...")
        logger.info(response)
        logger.info("=====================================")

        return response
