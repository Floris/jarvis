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
                "Create the file 'dump.txt'",
                "Use an Agent to create 5 characters and update dump.txt to save it",
                "Use an Agent to create 5 scenes and update dump.txt to save it",
                "Use an Agent to create 5 plot points and update dump.txt to save it",
                "Use the information from the dump.txt other files to write the book to write the 1st chapter 'chapter_1.txt'.",
                "Use the information from the dump.txt other files to write the book to write the 2nd chapter 'chapter_2.txt'.",
                "Use the information from the dump.txt other files to write the book to write the 3rd chapter 'chapter_3.txt'.",
                "Use the information from the dump.txt other files to write the book to write the 4th chapter 'chapter_4.txt'.",
                "Use the information from the dump.txt other files to write the book to write the 5th chapter 'chapter_5.txt'.",
                "Use the information from the dump.txt other files to write the book to write the final chapter 'chapter_final.txt'.",
                "Shutdown after achieving the goal.",
            ],
        ),
        user_input=triggering_prompt,
        message_history=[],
    )
    ai.start()


if __name__ == "__main__":
    main()
