from helpers.chat import generate_chat
from helpers.utils import is_int
from schemas import MessageDict

from settings.settings import gpt_model


def start_agent(name: str, task: str, prompt: str, model=gpt_model) -> str:
    """Start an agent with a given name, task, and prompt
    Args:
        name (str): The name of the agent
        task (str): The task of the agent
        prompt (str): The prompt for the agent
        model (str): The model to use for the agent
    Returns:
        str: The response of the agent
    """

    first_message = f"""You are {name}.  Respond with: "Acknowledged"."""

    # Create agent
    key, ack = agent_manager.create_agent(task, first_message, model)

    # Assign task (prompt), get response
    agent_response = agent_manager.message_agent(key, prompt)

    return f"Agent {name} created with key {key}. First response: {agent_response}"


def message_agent(key: str, message: str) -> str:
    """Message an agent with a given key and message"""

    # Check if the key is a valid integer
    if is_int(key) is False:
        return "Invalid key, must be an integer."

    return agent_manager.message_agent(int(key), message)


def list_agents():
    """List all agents
    Returns:
        str: A list of all agents
    """
    return "List of agents:\n" + "\n".join(
        [f"{str(x[0])}: {x[1]}" for x in agent_manager.list_agents()]
    )


def delete_agent(key: str) -> str:
    """Delete an agent with a given key
    Args:
        key (str): The key of the agent to delete
    Returns:
        str: A message indicating whether the agent was deleted or not
    """
    result = agent_manager.delete_agent(key)
    return f"Agent {key} deleted." if result else f"Agent {key} does not exist."


class AgentManager:
    def __init__(self):
        self.next_key = 0
        self.agents: dict[
            int, tuple[str, list[MessageDict], str]
        ] = {}  # key, (task, full_message_history, model)

    def create_agent(
        self, task: str, prompt: str, model="gpt-3.5-turbo"
    ) -> tuple[int, str]:
        conversation: list[MessageDict] = [
            {"role": "user", "content": prompt},
        ]

        conversation, _ = generate_chat(conversation=conversation, model=model)

        key = self.next_key
        self.next_key += 1

        self.agents[key] = (task, conversation, model)

        return key, conversation[-1]["content"]

    def message_agent(self, key: str | int, message: str) -> str:
        """Send a message to an agent and return its response"""
        task, conversation, model = self.agents[int(key)]

        # Add user message to message history before sending to agent
        conversation.append({"role": "user", "content": message})

        # Start GPT instance
        conversation, _ = generate_chat(
            conversation=conversation,
            model=model,
        )

        return conversation[-1]["content"]

    def list_agents(self) -> list[tuple[str | int, str]]:
        """Return a list of all agents
        Returns:
            A list of tuples of the form (key, task)
        """

        # Return a list of agent keys and their tasks
        return [(key, task) for key, (task, _, _) in self.agents.items()]

    def delete_agent(self, key: str | int) -> bool:
        """Delete an agent from the agent manager
        Args:
            key: The key of the agent to delete
        Returns:
            True if successful, False otherwise
        """

        try:
            del self.agents[int(key)]
            return True
        except KeyError:
            return False


agent_manager = AgentManager()
