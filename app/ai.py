import json
import logging
from typing import TypedDict

from agent import Agent
from coding_agent import CodingAgent
from helpers.chat import generate_chat
from helpers.file_helpers import append_to_file, read_file, write_to_file
from prompts.prompts import get_prompt
from schemas import MessageDict

logger = logging.getLogger()


class ThoughtsDict(TypedDict):
    text: str
    reasoning: str
    plan: str
    criticism: str


class CommandDict(TypedDict):
    name: str
    args: dict[str, str]


class CommunicationStateDict(TypedDict):
    past: str
    present: str
    future: str


class ResponseDict(TypedDict):
    thoughts: ThoughtsDict
    command: CommandDict
    communication_state: CommunicationStateDict


def execute_prompt(generated_prompt: str) -> str:
    conversation: list[MessageDict] = [
        {"role": "user", "content": generated_prompt},
    ]
    conversation, _ = generate_chat(conversation=conversation, temperature=0.0)
    return conversation[-1]["content"]


class AI(Agent):
    """
    A class object that contains the configuration information for the AI
    Attributes:
        ai_name (str): The name of the AI.
        ai_role (str): The description of the AI's role.
        ai_goals (list): The list of objectives the AI is supposed to complete.
    """

    def __init__(
        self,
        ai_name: str,
        ai_role: str,
        ai_goals: list | None = [],
    ) -> None:
        """
        Initialize a class instance
        Parameters:
            ai_name (str): The name of the AI.
            ai_role (str): The description of the AI's role.
            ai_goals (list): The list of objectives the AI is supposed to complete.
        Returns:
            None
        """
        if ai_goals is None:
            ai_goals = []

        self.ai_name = ai_name
        self.ai_role = ai_role
        self.ai_goals = ai_goals

        self.text: str = ""
        self.reasoning: str = ""
        self.plan: str = ""  # \n separated list of steps
        self.criticism: str = ""

        self.communication_state: CommunicationStateDict = CommunicationStateDict(
            past="", present="", future=""
        )
        self.command: CommandDict = {"name": "", "args": {}}

        self.learnings: str = ""

        self.read_file_name: str = ""
        self.read_file_data: str = ""

    def construct_prompt(self) -> str:
        """
        Construct a prompt string based on the AI's configuration.
        Parameters:
            None
        Returns:
            full_prompt (str): A string containing the initial prompt for the user
              including the ai_name, ai_role and ai_goals.
        """

        prompt_start = (
            "Your decisions must always be made independently without"
            " seeking user assistance. Play to your strengths as an LLM and pursue"
            " simple strategies with no legal complications."
            ""
        )

        # Construct full prompt
        full_prompt = (
            f"You are {self.ai_name}, {self.ai_role}\n{prompt_start}\n\nGOALS:\n\n"
        )

        # ai_goals
        for i, goal in enumerate(self.ai_goals):
            full_prompt += f"{i+1}. {goal}\n"

        # in the new prompt present is the past and future is the present
        if self.communication_state["present"] != "":
            full_prompt += f"\nPAST:\n{self.communication_state['present']}\n"
        if self.communication_state["future"] != "":
            full_prompt += f"\nPRESENT:\n{self.communication_state['future']}\n"

        if self.learnings != "":
            full_prompt += f"\nLEARNINGS:\n{self.learnings}\n"

        if self.read_file_name != "":
            full_prompt += f"\n{self.read_file_name}:\n{self.read_file_data}\n"
            self.read_file_name = ""  # reset read_file_name
            self.read_file_data = ""  # reset read_file_data

        full_prompt += f"\n\n{get_prompt()}"
        return full_prompt

    def log_thougths(self):
        logger.info("=====================================")
        logger.info("Current thoughts:")
        logger.info(f"Text: \n{self.text}\n\n")
        logger.info(f"Reasoning: \n{self.reasoning}\n\n")
        logger.info(f"Plan: \n{self.plan}\n\n")
        logger.info(f"Criticism: \n{self.criticism}\n\n")
        logger.info(f"Command: \n{self.command}\n\n")
        logger.info(f"Communication_state: \n{self.communication_state}\n\n")
        logger.info("=====================================")

    def handle_command(self) -> bool:
        """
        handles command
        Return if the agent should stop
        """

        shutdown = False

        if self.command["name"] == "shutdown":
            shutdown = True

        elif self.command["name"] == "do_nothing":
            pass

        elif self.command["name"] == "ask_ai_question":
            self.learnings += f'- {execute_prompt(self.command["args"]["prompt"])}\n'

        elif self.command["name"] == "start_coding_agent":
            agent_response = CodingAgent(
                name=self.command["args"]["name"],
                project_structure_file_name=self.command["args"]["file"],
            ).start()
            self.learnings += f"- {agent_response}\n"

        elif self.command["name"] in ["append_to_file", "append_code_to_file"]:
            append_to_file(
                filename=self.command["args"]["file"],
                text=self.command["args"]["data"],
            )

        elif self.command["name"] in [
            "write_to_file",
            "create_file",
            "save_code_to_file",
            "create_code",
        ]:
            write_to_file(
                filename=self.command["args"]["file"],
                text=self.command["args"]["text"],
            )

        elif self.command["name"] == "read_file":
            file_data = read_file(filename=self.command["args"]["file"])
            # Append the file data to the last learnings
            self.read_file_name = self.command["args"]["file"]
            self.read_file_data = file_data

        else:
            print(f"Command {self.command['name']} not recognized.")

        return shutdown

    def start(self) -> str:
        logger.info("=====================================")
        logger.info(f"Starting agent {self.ai_name}")
        logger.info(f"Role: {self.ai_role}")
        logger.info(f"Goals: {self.ai_goals}")
        logger.info("=====================================")

        while True:
            prompt = self.construct_prompt()
            response: ResponseDict = json.loads(execute_prompt(prompt))

            self.text = response["thoughts"]["text"]
            self.plan = response["thoughts"]["plan"]
            self.reasoning = response["thoughts"]["reasoning"]
            self.criticism = response["thoughts"]["criticism"]
            self.command = response["command"]
            self.communication_state = response["communication_state"]

            self.log_thougths()

            if "reflection" in self.command["args"]:
                self.learnings += f'- {self.command["args"]["reflection"]}\n'
            else:
                self.learnings += f'- {self.command["args"]["reason"]}\n'

            input("Press enter to continue...")
            shutdown = self.handle_command()

            if shutdown:
                break

        logger.info("=====================================")
        logger.info(f"Shutting down agent {self.ai_name}...")
        logger.info(("last learnings", self.learnings))
        logger.info("=====================================")
        return self.learnings
