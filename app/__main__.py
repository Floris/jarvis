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
    ai = AI(
        name="AI69",
        prompt=construct_prompt(
            "AI69",
            "a tech startup CTO, looking to create a new tech product!",
            [
                "Create your own game in JavaScript. You are in control, and you can do anything you want. ",
                "Ask an Agent to come up with a game idea. ",
                "Ask the Agent to create the code for the game.",
                "Keep iterating until you have a game you like.",
                "Shutdown after achieving the goal.",
            ],
        ),
        user_input=triggering_prompt,
        message_history=[],
    )
    ai.start()


if __name__ == "__main__":
    main()
