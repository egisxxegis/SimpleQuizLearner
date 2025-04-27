import json
from random import shuffle
import _types
from os import path

from _quizutils import get_correct_indexes, is_answer_correct
from PIL import Image
import re


def get_tasks_v2(*, full_file_path: str, its_folder: str):
    tasks: list[_types.TaskV2] = []
    with open(full_file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        tasks.extend([_types.TaskV2(**task) for task in content])
    for task in tasks:
        if task.random_picture_from is not None:
            task.random_picture_from = [
                path.join(its_folder, picture_path)
                for picture_path in task.random_picture_from
            ]
        task.number = path.basename(its_folder)
    return [_types.TaskV2.model_validate(task) for task in tasks]


def main(tasks: list[_types.TaskV2], scores: _types.Scores):
    i_range = [x for x in range(0, len(tasks))]
    shuffle(i_range)
    for i in i_range:
        task = tasks[i]
        print("\n------------------------------------------------------------------")
        print(
            f"(score: {scores.right}/{scores.total}) Page {task.number} question {task.original_num}."
        )
        print(f"{task.question}")
        print(f"\n")
        answer_indexes = [x for x in range(0, len(task.choices))]
        shuffle(answer_indexes)
        for ii in range(len(answer_indexes)):
            an = task.choices[answer_indexes[ii]]
            _id = (
                f"{ii + 1}."
                if task.option_type == "MULTI"
                else f"{_types.LETTERS[ii]})"
            )
            print(f"{_id} {an}")
        correct_index_nums = get_correct_indexes(
            answer_indexes, ",".join(str(x) for x in task.answers_num)
        )
        if (
            isinstance(task.random_picture_from, list)
            and len(task.random_picture_from) > 0
        ):
            correct_num = correct_index_nums[0]
            picture_path = task.random_picture_from[
                min(len(task.random_picture_from) - 1, correct_num - 1)
            ]
            print("--------------------------- Opening an image. ")
            Image.open(picture_path).show()
        multianswer_suffix = " (_MULTICHOICE_) " if task.option_type == "MULTI" else ""
        user_guess = input(f"Your choice? {multianswer_suffix}- ")
        # continue here
        user_guess = user_guess.upper()
        user_guess = ",".join(
            "".join(
                re.sub(
                    rf"[^1-9{_types.LETTERS[0]}-{_types.LETTERS[-1]}]", "", user_guess
                ).split()
            )
        )
        for letter in _types.LETTERS:
            user_guess = user_guess.replace(
                letter, str(_types.LETTERS.index(letter) + 1)
            )
        if is_answer_correct(user_guess, correct_index_nums):
            print("------Correct")
            scores.right += 1
        else:
            transformer = lambda x: (
                str(x)
                if task.option_type == "MULTI" or x >= len(_types.LETTERS)
                else f"{_types.LETTERS[x-1]})"
            )
            print(
                f"------Incorrect. Right answer{'s were' if task.option_type == "MULTI" else ' was'} "
                f"{', '.join([transformer(x) for x in correct_index_nums])}."
            )
            print(task.comment or "")
        scores.total += 1

        input("\n-------Enter to continue\n")
