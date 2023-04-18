import logging
import sys

import openai
from agent.ai import AI
from helpers.fancy_logging import ColoredLogRecord
from prompts.prompts import construct_prompt

from settings import settings

openai.api_key = settings.api_key

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logging.setLogRecordFactory(ColoredLogRecord)
logger.addHandler(console_handler)


def main():
    triggering_prompt = (
        "Determine which next command to use, and respond using the"
        " format specified above:"
    )
    # ai = AI(
    #     name="AI69",
    #     next_action_count=0,
    #     prompt=construct_prompt(
    #         "AI69",
    #         "a CTO tasked creating a backend system for a cryptocurrency exchange. It does not have to be tested or deployed.",
    #         [
    #             "Create an Agent that thinks about what backend functionalities the cryptocurrency exchange should have and save it to file 'functionalities.txt'.",
    #             "Create an Agent that thinks about the technology stack of the cryptocurrency exchange save it to file 'stack.txt'.",
    #             "Create an Agent that thinks about the project structure of the cryptocurrency exchange save it to file 'project_structure.txt'.",
    #             "Generate and save the code. Use multiple Agents to generate the code for the project structure."
    #             "Shutdown after achieving the goal.",
    #         ],
    #     ),
    #     user_input=triggering_prompt,
    #     message_history=[],
    # )
    ai = AI(
        name="AI69",
        next_action_count=0,
        prompt=construct_prompt(
            "AI69",
            "a Writer tasked with writing a new book.",
            [
                "Use an Agent to create 5 characters and save it to a file",
                "Use an Agent to create 5 scenes and save it to a file",
                "Use an Agent to create 5 plot points and save it to a file",
                "Read the files and use an Agent to write the book, save it to a file when done."
                "Shutdown after achieving the goal.",
            ],
        ),
        user_input=triggering_prompt,
        message_history=[],
    )
    ai.start()


if __name__ == "__main__":
    main()
