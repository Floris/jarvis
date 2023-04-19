import logging
import sys

import openai
from ai.ai import AI
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
    ai = AI(
        name="AI69",
        prompt=construct_prompt(
            "AI69",
            "a tech startup CTO, looking to create a new tech product!",
            [
                "Use an GPT Agent to come up with a game idea. The idea should be something you can create in JavaScript & I expect a minimum of 200 words.",
                "Save the idea to a file called idea.txt.",
                "Use a Coding Assistant to create code for the file 'idea.txt'.",
                "Shutdown after achieving the goal.",
            ],
        ),
        user_input=triggering_prompt,
    )
    ai.start()


if __name__ == "__main__":
    main()
