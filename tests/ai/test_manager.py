import pytest

from app.ai.manager import AgentManager
from tests.mocks.chat import mock_generate_chat


@pytest.fixture
def agent_manager():
    agent_manager = AgentManager()

    # Create an agent
    task = "Sample Task"
    prompt = "Sample Prompt"
    key, _ = agent_manager.create_agent(task, prompt)

    return agent_manager


def test_create_agent(agent_manager):
    task = "Test task"
    prompt = "Test prompt"
    model = "gpt-3.5-turbo"

    key, response = agent_manager.create_agent(task, prompt, model)
    assert key == 1
    assert isinstance(response, str)
    assert agent_manager.agents[key][0] == task
    assert agent_manager.agents[key][2] == model


@mock_generate_chat()
def test_message_agent(agent_manager):
    key = 0

    response = agent_manager.message_agent(key, "Test message")
    assert isinstance(response, str)
    assert (
        agent_manager.agents[key][1][-1]["content"]
        == "\n\nHello there, this is a mocked response?"
    )


def test_list_agents(agent_manager):
    agents = agent_manager.list_agents()
    assert len(agents) == 1
    assert agents[0][0] == 0
    assert agents[0][1] == "Sample Task"


def test_delete_agent(agent_manager):
    key = 0
    assert agent_manager.delete_agent(key) is True
    assert agent_manager.agents.get(key) is None
