import json
import logging
from typing import Any, Literal, TypedDict

from agent.manager import delete_agent, list_agents, message_agent, start_agent
from helpers.chat import generate_chat
from helpers.file_helpers import append_to_file, read_file, write_to_file
from schemas import MessageDict

logger = logging.getLogger()


class ShutDown(Exception):
    pass


class ThoughtsDict(TypedDict):
    summary: str
    text: str
    reasoning: str
    plan: str
    criticism: str


class CommandDict(TypedDict):
    name: str
    args: dict[str, str]


class ResponseDict(TypedDict):
    thoughts: ThoughtsDict
    command: CommandDict


def create_conversation_message(
    role: Literal["system", "user"], content: str
) -> MessageDict:
    return {"role": role, "content": content}


def generate_context(prompt: str, relevant_memory: str) -> list[MessageDict]:
    context = [
        create_conversation_message("system", prompt),
        create_conversation_message(
            "system",
            f"This reminds you of these events from your past:\n{relevant_memory}\n\n",
        ),
    ]
    return context


def execute_prompt(generated_prompt: str) -> str:
    conversation: list[MessageDict] = [
        {"role": "user", "content": generated_prompt},
    ]
    conversation, _ = generate_chat(conversation=conversation, temperature=0.0)
    return conversation[-1]["content"]


def handle_command(name: str, args: dict) -> Any:
    if name == "shutdown":
        raise ShutDown("Shutdown command received.")

    elif name == "ask_ai_question":
        response = f'- {execute_prompt(args["prompt"])}\n'

    elif name == "start_agent":
        return start_agent(args["name"], task=args["task"], prompt=args["prompt"])

    elif name == "message_agent":
        return message_agent(args["key"], args["message"])

    elif name == "list_agents":
        return list_agents()

    elif name == "delete_agent":
        return delete_agent(args["key"])

    elif name in ["append_to_file", "update_file"]:
        append_to_file(
            filename=args["file"],
            text=args["text"],
        )
        response = f'Updated file: {args["file"]}'

    elif name in [
        "write_to_file",
        "create_file",
    ]:
        write_to_file(
            filename=args["file"],
            text=args["text"],
        )
        response = f'Saved data to file: {args["file"]}'

    elif name == "read_file":
        response = read_file(filename=args["file"])

    elif name == "do_nothing":
        return "No action performed."

    else:
        response = "Command not recognized."

    return response


class AI:
    def __init__(
        self,
        name: str,
        next_action_count: int,
        prompt: str,
        user_input: str,
        message_history: list[MessageDict] = [],
    ) -> None:
        self.name = name
        self.next_action_count = next_action_count
        self.prompt = prompt
        self.user_input = user_input
        self.message_history = message_history
        self.memory: list[str] = []

    def chat(self) -> ResponseDict:
        relevant_memory = (
            "" if len(self.message_history) == 0 else str(self.memory[-6:])
        )

        conversation = generate_context(
            prompt=self.prompt,
            relevant_memory=relevant_memory,
        )
        conversation.append(create_conversation_message("user", self.user_input))

        # add user input message to history
        self.message_history.append(conversation[-1])

        conversation, _ = generate_chat(conversation=conversation, temperature=0.0)

        # add to response history
        self.message_history.append(conversation[-1])

        return json.loads(conversation[-1]["content"])

    def start(self):
        """Start AI loop"""
        logger.info(f"Starting AI {self.name}...")

        while True:
            input("Press enter to continue...")

            try:
                reply = self.chat()
            except ShutDown as e:
                logger.info(e)
                break

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
                result = f"Human feedback: {self.user_input}"
            else:
                self.user_input = "GENERATE NEXT COMMAND JSON"
                result = (
                    f"Command {reply['command']['name']} returned: "
                    f"{handle_command(name=reply['command']['name'], args=reply['command']['args'])}"
                )

            self.memory.append(
                f"\nAssistant Reply: {reply} "
                f"\nResult: {result} "
                f"\nHuman Feedback: {self.user_input} "
            )

            logger.info("====================")
            logger.info("Memory")
            logger.info(self.memory)
            logger.info("====================")

        logger.info("====================")
        logger.info(f"AI {self.name} shut down.")
        logger.info("====================")
