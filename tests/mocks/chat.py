from functools import wraps
from unittest.mock import patch

mock_response = {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "\n\nHello there, this is a mocked response?",
            },
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
}


def mock_generate_chat():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with patch("openai.ChatCompletion.create") as mock_generate_chat:
                mock_generate_chat.return_value = mock_response

                result = func(*args, **kwargs)

                mock_generate_chat.assert_called_once()
            return result

        return wrapper

    return decorator
