from unittest.mock import patch

import pytest

from app.ai.manager import AgentManager

mocked_openai_create_chatcompletion = {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "\n\nHello there, how may I assist you today?",
            },
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
}


@pytest.fixture
def agent_manager() -> AgentManager:
    agent_manager = AgentManager()

    # Create an agent
    task = "Sample Task"
    prompt = "Sample Prompt"

    with patch("openai.ChatCompletion.create") as mock_function:
        mock_function.return_value = mocked_openai_create_chatcompletion
        key, _ = agent_manager.create_agent(task, prompt)

    return agent_manager


def test_create_agent(agent_manager: AgentManager) -> None:
    task = "Test task"
    prompt = "Test prompt"
    model = "gpt-3.5-turbo"

    with patch("openai.ChatCompletion.create") as mock_function:
        mock_function.return_value = mocked_openai_create_chatcompletion
        key, response = agent_manager.create_agent(task, prompt, model)

    assert key == 1
    assert isinstance(response, str)
    assert agent_manager.agents[key][0] == task
    assert agent_manager.agents[key][2] == model


def test_message_agent(agent_manager: AgentManager) -> None:
    key = 0

    with patch("openai.ChatCompletion.create") as mock_function:
        mock_function.return_value = mocked_openai_create_chatcompletion
        response = agent_manager.message_agent(key, "Test message")

    assert isinstance(response, str)
    assert (
        agent_manager.agents[key][1][-1]["content"]
        == "\n\nHello there, how may I assist you today?"
    )


def test_list_agents(agent_manager: AgentManager) -> None:
    agents = agent_manager.list_agents()
    assert len(agents) == 1
    assert agents[0][0] == 0
    assert agents[0][1] == "Sample Task"


def test_delete_agent(agent_manager: AgentManager) -> None:
    key = 0
    assert agent_manager.delete_agent(key) is True
    assert agent_manager.agents.get(key) is None
