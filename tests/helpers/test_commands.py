from app.helpers.commands import append_generate_code, chat_commands
from app.schemas import MessageDict


def test_append_generate_code():
    conversation: list[MessageDict] = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi, how can I help you?"},
    ]

    updated_conversation = append_generate_code(conversation)

    assert len(updated_conversation) == 3
    assert updated_conversation[-1]["role"] == "user"
    assert (
        "Generate code for all the files in the project structure"
        in updated_conversation[-1]["content"]
    )
    assert (
        "File: {Project Name}/{path}/{filename}" in updated_conversation[-1]["content"]
    )
    assert (
        "Done: {Project Name}/{path}/{filename}" in updated_conversation[-1]["content"]
    )
    assert "---Finished---" in updated_conversation[-1]["content"]


def test_chat_commands():
    assert "create_code" in chat_commands
    assert chat_commands["create_code"] == append_generate_code
