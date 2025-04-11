import pydantic
from typing import Literal


class TaskV2(pydantic.BaseModel):
    number: int
    question: str
    choices: list[str]
    answers_i: list[int]
    picture_path: str | None = None
    comment: str | None = None


class SimpleAnswer(pydantic.BaseModel):
    raw: str
    question_num: int
    answer: Literal["A", "B", "C", "D", "E", "F"]


class SimpleQuestion(pydantic.BaseModel):
    raw: str
    question_num: int
    question: str
