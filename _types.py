import pydantic
from typing import Literal, Type

TypeAnswer = Literal["A", "B", "C", "D", "E", "F"]
TypeAnswerConversion = list[int] | Literal["all", "N/A"]
LETTERS: list[TypeAnswer] = ["A", "B", "C", "D", "E", "F"]


class TypeAnswerConverter:
    def __call__(self, answer: TypeAnswer, options_count: int) -> list[int]:
        raise NotImplementedError("I am only a placeholder")


class TaskV2(pydantic.BaseModel):
    number: int
    question: str
    choices: list[str]
    answers_num: list[int]
    option_type: Literal["AB", "MULTI"]
    original_num: int
    random_picture_from: str | None = None
    comment: str | None = None

    def get_answers(self) -> list[str]:
        return [self.choices[answer_num - 1] for answer_num in self.answers_num]


class SimpleAnswer(pydantic.BaseModel):
    raw: str
    question_num: int
    answer: TypeAnswer


class SimpleQuestion(pydantic.BaseModel):
    raw: str
    question_num: int
    question: str


class SimpleOption(pydantic.BaseModel):
    raw: str
    option_num: int
    option_id: str
    option: str


class SimplePage(pydantic.BaseModel):
    raw: str
    page_num: int


class SimpleTask(pydantic.BaseModel):
    answer: SimpleAnswer
    question: SimpleQuestion
    options: list[SimpleOption]


class SimpleChem(pydantic.BaseModel):
    raw: str
    chem_unscripted: str
