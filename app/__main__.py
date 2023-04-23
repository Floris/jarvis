import logging
import sys

import openai
from ai.ai import AI
from helpers.fancy_logging import ColoredLogRecord
from prompts.prompts import construct_prompt

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logging.setLogRecordFactory(ColoredLogRecord)
logger.addHandler(console_handler)


try:
    from settings import settings

    openai.api_key = settings.api_key
except ImportError as e:
    logger.exception(e)


def main() -> None:
    name = "AI"
    ai = AI(
        name=name,
        prompt=construct_prompt(
            name,
            "a tech startup CTO, looking to create a cryptocurrency trading bot.",
            [
                "Use an GPT Agent to brainstorm ideas for the bot.",
                "Use GPT Agent an GPT agent for feedback on the ideas. Do this until you have a good idea",
                "Once you have a good idea, use an GPT Agent to build out a plan for the bot."
                "Save the plan to a file called plan.txt.",
                "Use an GPT Agent to create pseudocode for the bot."
                "Shutdown after achieving the goal.",
            ],
        ),
        user_input=(
            "Determine which next command to use, and respond using the"
            " format specified above:"
        ),
    )
    ai.start()


if __name__ == "__main__":
    main()
