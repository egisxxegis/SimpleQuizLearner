from FileHandler import get_content, get_all_valid_folders
from os import path
from random import shuffle
from typing import Literal
import _quizerv2 as qv2
import _types
from _quizutils import get_correct_indexes, is_answer_correct
import re

from Task import Task

the_pil = True
if the_pil:
    from PIL import Image


def get_all_content():
    all_folders = get_all_valid_folders()
    all_content: list[Task] | list[_types.TaskV2] = []
    packs: list[list[Task] | list[_types.TaskV2]] = []
    filename = "questions.txt"
    filename_json = "questions.json"
    mode: None | Literal["json", "txt"] = None

    def sustain_mode(value: str, full_path: str):
        nonlocal mode
        if mode is None:
            mode = value
            return
        if mode != value:
            raise ValueError(
                "Do not mix json and txt files."
                + f" Found {value} in {full_path} even though we are in {mode} mode."
            )

    for folder in all_folders:
        the_path = path.join(folder, filename)
        if path.exists(the_path):
            sustain_mode("txt", folder)
        the_path2 = path.join(folder, filename_json)
        if path.exists(the_path2):
            sustain_mode("json", folder)
            the_path = the_path2
        if not path.exists(the_path):
            raise NameError(
                f"Found empty folder: {folder}. Please add questions to folder or delete the folder."
            )

        if mode == "txt":
            source = {"full_file_path": the_path}
            the_content = get_content(source, "%!%", folder)
            all_content += the_content
            packs.append(the_content)
        elif mode == "json":
            the_content = qv2.get_tasks_v2(full_file_path=the_path, its_folder=folder)
            all_content += the_content
            packs.append(the_content)
        else:
            raise NotImplementedError(f"Unknown mode: {mode}.")

    return all_content, packs


def main(content: list[Task], scores: _types.Scores):
    i_range = [x for x in range(0, len(content))]
    shuffle(i_range)
    for i in i_range:
        task = content[i]
        print("\n------------------------------------------------------------------")
        print(
            f"({i+1}/{len(content)}; your score: {scores.right}/{scores.total}) {task.question}"
        )
        print(f"\n")
        answer_indexes = [x for x in range(0, len(task.answers))]
        shuffle(answer_indexes)
        for ii in range(len(answer_indexes)):
            an = task.answers[answer_indexes[ii]]
            nl = "\n"
            print(f"{ii+1}. {an if an[-1] == nl else an + nl}")
        correct_index = get_correct_indexes(answer_indexes, task.answer_i)
        if task.has_picture and the_pil:
            print("--------------------------- Opening an image. ")
            Image.open(task.full_path_picture).show()
        multianswer_suffix = (
            "(input more than one answer (MULTICHOICE)) "
            if task.is_answer_multi
            else ""
        )
        user_guess = input(f"Your choice? {multianswer_suffix}- ")
        # continue here
        if is_answer_correct(user_guess, correct_index):
            print("------Correct")
            scores.right += 1
        else:
            print(
                f"------Incorrect. Right answer{'s were' if task.is_answer_multi else ' was'} "
                f"{', '.join([str(x) for x in correct_index])}."
            )
            print(task.comment)
        scores.total += 1

        input("\n-------Enter to continue\n")


if __name__ == "__main__":
    content, packs = get_all_content()
    score_factory = lambda: _types.Scores(right=0, total=0)
    scores = score_factory()

    def print_scores(is_prompt_ending=True):
        print("\n\n\n")
        print("--**--**-- Results --**--**--")
        print(f"--**-- Total questions: {scores.total}")
        print(f"--**-- Right answers:   {scores.right}")
        print(
            f"--**-- Magic score:     {scores.right}/{scores.total} = {scores.right / (scores.total or 1) * 100 : .2f}%"
        )
        print("\n\n")
        if is_prompt_ending:
            input("\n--**--**-- Enter to exit\n")

    if len(content) == 0 or isinstance(content[-1], Task):
        main(content, scores)
        print_scores()
    else:
        content2 = qv2.reduce_packs(packs)
        assert len(content) >= len(
            content2
        ), f"Reduced packs len {len(content2)} cant be longer than full dataset content {len(content)}"
        while len(content2) > 0:
            retryables = qv2.main(content2, scores)
            is_retryable = retryables and len(retryables) > 0
            print_scores(is_prompt_ending=not is_retryable)
            if is_retryable:
                while True:
                    print("\n")
                    print(f"Retry {len(retryables)} failed questions?")
                    print("A. Yes\nB. No and exit")
                    user_guess = qv2.normalize_user_guess(input(f"Your choice? - "))
                    if not user_guess in ["1", "2"]:
                        continue
                    if qv2.is_answer_correct(user_guess, [1]):
                        content2 = retryables
                        scores = score_factory()
                        break
                    else:
                        exit(0)
            else:
                content2 = []  # exhausted
