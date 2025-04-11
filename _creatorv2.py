import os
import json
import re

import _types


def get_answers(raw: str, lowest_num: int = 1):
    """
    59 – D
    60 – D
    133

    6 – C
    7 – D
    """
    pattern_num = r"\d+"
    pattern_answer = (
        r"[abcdefABCDEF]+"  # supplying '+' to prevent parsing '4. Define' as '4. D'
    )
    pattern_separator = r"[.\-–:]?"
    pattern = r"\s*".join(
        ["(", pattern_num, pattern_separator, pattern_separator, pattern_answer, ")"]
    )
    findings: list[str] = re.findall(pattern, raw)
    answers: list[_types.SimpleAnswer] = []
    for finding in findings:
        num = re.search(pattern_num, finding).group()
        answer = re.search(pattern_answer, finding).group()
        try:
            answers.append(
                _types.SimpleAnswer(
                    raw=finding, answer=answer.upper(), question_num=int(num)
                )
            )
        except ValueError:
            pass

    # possibly some noise from questions and from pagination.
    # thus search for sequence [1; x] in the end
    # 144 6 5 2 143 1 4 3 1
    # ---> 6 5 4 3 2 1
    answers_reverse = answers[::-1]
    num_to_answer = dict()
    for answer in answers_reverse:
        if answer.question_num not in num_to_answer:
            num_to_answer[answer.question_num] = answer
        else:
            pass  # discarded

    is_edited = True
    while is_edited:
        is_edited = False
        nums = list(num_to_answer.keys())
        nums.sort(reverse=True)
        for num in nums:
            if num == lowest_num:
                continue
            if num < lowest_num or num - 1 not in num_to_answer:
                num_to_answer.pop(num)
                is_edited = True

    values: list[_types.SimpleAnswer] = list(num_to_answer.values())
    return sorted(values, key=lambda x: x.question_num)


def _cut_answers(raw: str, answers: list[_types.SimpleAnswer]):
    assert len(answers) >= 2, "Not enough answers to parse questions."
    pattern_answers_start = answers[0].raw + r".{0,11}?" + answers[1].raw
    parts = re.split(pattern_answers_start, raw, 1)
    assert len(parts) == 2, "Cannot split questions and answers."
    body = re.split(r"atsak.{1,10}$", parts[0], 0, re.IGNORECASE)[0]
    return body


def get_questions(raw: str, answers: list[_types.SimpleAnswer]):
    body = " " + _cut_answers(raw, answers)

    """
    2. Kokie yra mėlynių vaisių ekstrakto poveikiai? 
    1. Antioksidacinis. 
    2. Priešuždegiminis. 
    3. Hipoglikeminis. 
    4. Lipidų metabolizmą reguliuojantis.
    """
    questions: list[_types.SimpleQuestion] = []
    for big_num in [answer.question_num for answer in answers][::-1]:
        pattern = f"[^a-zA-Z0-9]({big_num}" + r".{5,}?)[aA1][\.\-–\)]"
        qsearch = [found for found in re.finditer(pattern, body, re.DOTALL)][-1]
        assert qsearch, big_num
        body = body[: qsearch.start()]
        question = _types.SimpleQuestion(
            raw=qsearch.group(1),
            question_num=big_num,
            question=re.sub(
                f"{big_num}" + r"\s*[.\-–:]", "", qsearch.group(1), 1, re.DOTALL
            )
            .replace("\n", "")
            .replace("\r", "")
            .strip("\t "),
        )
        questions.append(question)
    return questions[::-1]


def loop_create():
    folder = input("Folder name: ")
    if os.path.exists(folder):
        print("Folder already exists. Bye")
    os.mkdir(folder)
    raw = input("Input full data with answer sheet.\n").strip("\r\n")
