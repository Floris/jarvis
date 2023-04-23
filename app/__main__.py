import logging
import sys

import openai
from ai.ai import AI
from helpers.fancy_logging import ColoredLogRecord
from prompts.prompts import construct_prompt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    ai_name = "Codebot"
    ai_role = "an AI trained to create coding products and assist with programming tasks. Generates code snippets based on user requirements. Identifies bugs and suggest fixes. Optimizes code for performance and readability."
    ai_goals = [
        "Generate a Python function to calculate the factorial of a number?",
        "Save the function to a file.",
        "Shutdown when the goal is achieved",
    ]
    initial_user_input = (
        "Determine which next command to use, and respond using the"
        " format specified above:"
    )
    ai_prompt = construct_prompt(ai_name, ai_role, ai_goals)
    codebot = AI(
        name=ai_name,
        prompt=ai_prompt,
        user_input=initial_user_input,
    )
    codebot.start()


if __name__ == "__main__":
    main()
