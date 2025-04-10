from FileHandler import get_content, get_all_valid_folders, fix_format_multianswer
from os import path
from random import shuffle

from Task import Task

the_pil = bool(input("Type anything to allow show images. (if there is any)"))
if the_pil:
    from PIL import Image


def get_all_content():
    all_folders = get_all_valid_folders()
    all_content = []
    for folder in all_folders:
        the_path = path.join(folder, "questions.txt")
        source = {"full_file_path": the_path}
        the_content = get_content(source, "%!%", folder)
        all_content += the_content

    return all_content


def get_correct_indexes(the_answer_indexes: list[int], real_answers_i: str):
    real_answers_i = (
        real_answers_i if isinstance(real_answers_i, str) else str(real_answers_i)
    )
    multi_explode = [int(x) for x in real_answers_i.split(",") if x.isnumeric()]
    correct_indexes = []
    for iii in range(0, len(the_answer_indexes)):
        if the_answer_indexes[iii] + 1 in multi_explode:  # dp not +1 for old versions
            correct_indexes.append(iii + 1)
    return correct_indexes


def is_answer_correct(the_input: str, the_correct_indexes: list[int]):
    the_input = fix_format_multianswer(the_input)
    the_chosens = [int(x) for x in the_input.split(",") if x.isnumeric()]
    the_right_ones = [int(x) for x in the_correct_indexes]
    the_chosen = the_chosens if len(the_chosens) > 0 else [0]
    the_right_ones = the_right_ones if len(the_chosen) > 0 else [0]
    the_right_ones.sort()
    the_chosens.sort()
    return the_right_ones == the_chosens


if __name__ == "__main__":
    content = get_all_content()

    i_range = [x for x in range(0, len(content))]
    shuffle(i_range)
    right = 0
    total = 0
    for i in i_range:
        task: Task = content[i]
        print("\n------------------------------------------------------------------")
        print(f"({i+1}/{len(content)}; your score: {right}/{total}) {task.question}")
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
            right += 1
        else:
            print(
                f"------Incorrect. Right answer{'s were' if task.is_answer_multi else ' was'} "
                f"{', '.join([str(x) for x in correct_index])}."
            )
            print(task.comment)
        total += 1

        input("\n-------Enter to continue\n")
    print("\n\n\n")
    print("--**--**-- Results --**--**--")
    print(f"--**-- Total questions: {total}")
    print(f"--**-- Right answers:   {right}")
    print(f"--**-- Magic score:     {right}/{total} = {right / total * 100 : .2f}%")
    print("\n\n")
    input("\n--**--**-- Enter to exit\n")
