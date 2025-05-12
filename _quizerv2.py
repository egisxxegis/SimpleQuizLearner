import json
from random import shuffle
import _creatorv2
import _types
from os import path

from _quizutils import get_correct_indexes, is_answer_correct
from PIL import Image, ImageFile
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


def get_folder_indexes(
    nums_str: str, topics: list[str], folders_per_topic: int
) -> list[int] | None:
    assert (
        0 < len(topics) < len(_types.INTRO_NUMBERS)
    ), f"Sorry, too many/little topics. Len={len(topics)}"
    allowed_nums = _types.INTRO_NUMBERS[0 : len(topics)]
    chosen_nums = _creatorv2._parse_multis(
        nums_str, _types._MIN1, _types._MAX1, _types._MIN2, _types._MAX2
    )
    if chosen_nums is None:
        return None
    chosen_nums, special = _creatorv2._intify_multis(chosen_nums, allowed_nums)
    if special == "*":
        chosen_nums = [x for x in range(1, len(topics) + 1)]
    if len(chosen_nums) == 0:
        print("No topics chosen. Please try again.")
        return None

    indexes: list[int] = []
    for chosen_num in set(chosen_nums):
        try:
            base_i = chosen_num - 1
        except TypeError:
            print(f"Please check the input - symbol `{chosen_num}` is not supported.")
            return None
        for i in range(0, folders_per_topic):
            # 0 -> 0, 1, 2
            # 1 -> 3, 4, 5
            indexes.append(base_i * folders_per_topic + i)
    return sorted(indexes)


def reduce_packs(packs: list[list[_types.TaskV2]]) -> list[_types.TaskV2]:
    _path = "_hello.json"
    tasks = []
    if not path.exists(_path):
        for pack in packs:
            tasks.extend(pack)
        return tasks
    with open(_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    intro = _types.Intro(**content)
    while True:
        print("---  " + intro.question + "  ---")
        for i, answer in enumerate(intro.answers):
            print(f"{_types.INTRO_NUMBERS[i]}. {answer}")
        print("\n")
        user_guess = input(
            "Choose topics (type asterisk * to select all) (_MULTICHOICE_): "
        )
        indexes = get_folder_indexes(user_guess, intro.answers, intro.folders_per_topic)
        if indexes is None:
            print("\n")
            continue
        assert indexes[-1] < len(
            packs
        ), f"Index out of range: {indexes=} len(packs)={len(packs)}"
        for _index in indexes:
            tasks.extend(packs[_index])
        return tasks


def main(tasks: list[_types.TaskV2], scores: _types.Scores):
    i_range = [x for x in range(0, len(tasks))]
    shuffle(i_range)
    for i in i_range:
        image_handle: None | ImageFile.ImageFile = None
        task = tasks[i]
        print("\n------------------------------------------------------------------")
        question_id = f"Page {task.number} question {task.original_num}."
        print(
            f"(score: {scores.right}/{scores.total} out of {len(tasks)}) {question_id}"
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
            image_handle = Image.open(picture_path)
            image_handle.show(question_id)
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

        input(
            f"\n-------Enter to continue\n{'also remember to close the image\n' if image_handle is not None else ''}"
        )
        if image_handle is not None:
            image_handle.close()
