from typing import Literal, TypedDict

from pydantic import BaseModel


class Message(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Literal["length", "stop", "eos"]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ApiResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: list[Choice]
