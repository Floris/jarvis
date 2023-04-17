from abc import ABC, abstractmethod


class Agent(ABC):
    """
    Abstract Base class for all agents.

    Agents are specializations of the AI that are used to perform specific tasks.
    For example, the Coding Agent is used to generate code for a project structure.
    """

    @abstractmethod
    def construct_prompt(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> str:
        raise NotImplementedError
