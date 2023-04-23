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
            "a tech startup CTO, looking to create a new tech product!",
            [
                "Use an GPT Agent to come up with a game idea. The idea should be something you can create in JavaScript & I expect a minimum of 200 words.",
                "Use GPT Agent an GPT agent for feedback on the idea.",
                "Once the idea is approved, use an GPT Agent to come up with a game plan. The plan should be something you can create in JavaScript & I expect a minimum of 200 words.",
                "Save the plan to a file called plan.txt.",
                "Shutdown after achieving the goal.",
            ],
        ),
        user_input=(
            "Determine which next command to use, and respond using the"
            " format specified above:"
        ),
    )
    ai.start()

    name = "PSEUDOCODE_AI"
    ai = AI(
        name=name,
        prompt=construct_prompt(
            name,
            "a tech startup CTO, building a new tech product!",
            [
                "Read plan.txt & use an GPT Agent to create pseudocode for the game plan.",
                "Save the pseudocode to a file.",
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
