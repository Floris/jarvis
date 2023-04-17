import logging
import sys

import openai
from ai import AI
from helpers.fancy_logging import ColoredLogRecord

from settings import settings

openai.api_key = settings.api_key

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logging.setLogRecordFactory(ColoredLogRecord)
logger.addHandler(console_handler)


def main():
    ai = AI(
        "AI69",
        "a CTO tasked with managing the development of a cryptocurrency exchange.",
        [
            "Create backend_project.txt",
            "Create a detailed project description and save it to file 'backend_project.txt'.",
            "Think about what backend functionalities the cryptocurrency exchange should have and save it to file 'backend_project.txt'.",
            "Based on the backend functionalities create a technology stack, update the file 'backend_project.txt'.",
            "Based on the backend functionalities create the project structure, update the file 'backend_project.txt'.",
            "Based on all of the information saved into the file 'backend_project.txt', read it and create multiple smaller projects and save it into a multiple new (task) files."
            "Delegate all the task files to a CodingAgent.",
            "Shutdown after achieving the goal.",
        ],
    )
    ai.start()


if __name__ == "__main__":
    main()
