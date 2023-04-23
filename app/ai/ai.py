import json
import logging

from exceptions import ShutDown
from helpers.chat import create_conversation_message, generate_chat
from helpers.commands import handle_command
from memory.memory import WeaviateMemory
from schemas import MessageDict, ResponseDict

logger = logging.getLogger()


def generate_context(prompt: str, relevant_memory: str) -> list[MessageDict]:
    """
    Generate a context list of messages for the AI, including the prompt and relevant memory.

    Args:
        prompt (str): The prompt for the AI.
        relevant_memory (str): Relevant memory for the AI to recall.

    Returns:
        list[MessageDict]: A list of messages to form the context.
    """
    if relevant_memory == "":
        return [
            create_conversation_message("system", prompt),
        ]

    return [
        create_conversation_message("system", prompt),
        create_conversation_message(
            "system",
            f"This reminds you of these events from your past:\n{relevant_memory}\n\n",
        ),
    ]


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in the given text based on spaces.

    Args:
        text (str): The text to count tokens in.

    Returns:
        int: The number of tokens in the text.
    """
    tokens = text.split()
    return len(tokens)


class AI:
    """
    Initialize the AI instance.

    Args:
        name (str): The name of the AI.
        prompt (str): The initial prompt for the AI.
        user_input (str): The initial user input.
        message_history (list[MessageDict], optional): The message history. Defaults to [].
    """

    def __init__(
        self,
        name: str,
        prompt: str,
        user_input: str,
        message_history: list[MessageDict] = [],
    ) -> None:
        self.name = name
        self.prompt = prompt
        self.user_input = user_input
        self.message_history: list[MessageDict] = message_history

    def chat(self) -> ResponseDict:
        """
        Conduct a chat with the AI and return the response.

        Returns:
            ResponseDict: The AI-generated response.
        """
        relevant_memory = self.memory.get_relevant(
            data=str(self.message_history[-9:]), num_relevant=10
        )

        conversation = generate_context(
            prompt=self.prompt,
            relevant_memory=relevant_memory,
        )

        current_tokens_used = count_tokens(str(conversation))

        # remove memories until we are under 2100 tokens
        while current_tokens_used > 2100:
            relevant_memory = relevant_memory[:-1]
            conversation = generate_context(
                prompt=self.prompt,
                relevant_memory=relevant_memory,
            )
            current_tokens_used = count_tokens(str(conversation))

        conversation.append(create_conversation_message("user", self.user_input))

        # add user input message to history
        self.message_history.append(conversation[-1])

        conversation, _ = generate_chat(conversation=conversation, temperature=0.0)

        # add to response history
        self.message_history.append(conversation[-1])

        return json.loads(conversation[-1]["content"])

    def start(self) -> None:
        with WeaviateMemory(ai_name=self.name) as memory:
            self.memory = memory
            self.start_loop()

    def start_loop(self) -> None:
        """
        Start the AI loop, where the AI processes user input and returns responses.
        This loop continues until the "shutdown" command is received.

        In each iteration of the loop, the AI generates a response based on the user input
        and the command associated with the response. If the command is "human_feedback",
        the user provides feedback, otherwise, the AI executes the command and stores the
        results in its memory.
        """

        logger.info(f"Starting AI {self.name}...")

        while True:
            input("Press enter to continue...")

            reply = self.chat()

            logger.info("====================")
            logger.info("Thoughts \n")
            logger.info(reply["thoughts"])
            logger.info("====================")

            logger.info("====================")
            logger.info("Command \n")
            logger.info(reply["command"]["name"])
            logger.info(reply["command"]["args"])
            logger.info("====================")

            if reply["command"]["name"] == "human_feedback":
                self.user_input = input(
                    f'Question: {reply["command"]["args"]["question"]} \n Answer: '
                )
                self.user_input += "\n\n GENERATE NEXT COMMAND JSON"
                result = f"Human feedback: {self.user_input}"
            else:
                self.user_input = "GENERATE NEXT COMMAND JSON"
                try:
                    result = (
                        f"Command {reply['command']['name']} returned: "
                        f"{handle_command(name=reply['command']['name'], args=reply['command']['args'], memory=self.memory)}"
                    )
                except ShutDown:
                    break

            memory_text = (
                f"\nAssistant Reply: {reply} "
                f"\nResult: {result} "
                f"\nHuman Feedback: {self.user_input} "
            )
            self.memory.add(data=memory_text)

        logger.info("====================")
        logger.info(f"AI {self.name} shut down.")
        logger.info("====================")
