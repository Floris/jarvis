from typing import Literal, TypedDict

from pydantic import BaseModel


class MessageDict(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class ChoiceSchema(BaseModel):
    index: int
    message: MessageDict
    finish_reason: Literal["length", "stop", "eos"]


class UsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ApiResponseSchema(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: UsageSchema
    choices: list[ChoiceSchema]


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
