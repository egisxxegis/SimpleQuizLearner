from os import path, mkdir, scandir, getcwd
from Task import Task


def create_if_not_exists(the_source):
    if not path.exists(the_source["folder"]):
        mkdir(the_source["folder"])
    if not path.exists(the_source["full_file_path"]):
        open(the_source["full_file_path"], "x")


def get_content(the_source, the_limiter, its_folder=""):
    the_file = open(the_source["full_file_path"], "r", encoding="utf-8")
    the_raw_content = the_file.read()
    the_content: list[Task] = []
    the_i = -1
    the_x = 0
    the_task = Task()
    if len(the_raw_content) < 3:
        return the_content
    for fragment in the_raw_content.split(the_limiter):
        if the_i == 0:
            the_task = Task()
            the_task.number = int(fragment)
        elif the_i == 1:
            the_picture_path = fragment
            if the_picture_path != "0":
                the_task.set_picture(path.join(its_folder, the_picture_path))
        elif the_i == 2:
            the_task.question = fragment
        elif the_i == 3:
            the_x = int(fragment)
        elif the_i == 4:
            the_x -= 1
            if the_x >= 0:
                the_task.answers.append(fragment)
                if the_x == 0:
                    the_i += 1
                continue
        elif the_i == 5:
            if fragment.count(",") > 0:
                # multi
                the_task.answer_i = fragment
                the_task.is_answer_multi = True
            else:
                the_task.answer_i = fragment
        elif the_i == 6:
            the_task.comment = fragment

        the_i += 1
        if the_i == 7:
            the_content.append(the_task)
            the_i = 0
    return the_content


def fix_format_multianswer(answer_string: str):
    answer_string = answer_string if len(answer_string) > 0 else "0"
    rates = [0, 0, 0]
    rates[0] = answer_string.count(".")
    rates[1] = answer_string.count(",")
    rates[2] = answer_string.count(" ")
    if max(rates) == rates[2]:
        answer_string = (
            answer_string.replace(".", "").replace(",", "").replace(" ", ",")
        )
    elif max(rates) == rates[1]:
        answer_string = answer_string.replace(".", "").replace(" ", "")
    else:
        if rates[0] == 1:
            # there is no multianswer
            return answer_string.replace(".", "").replace(",", "").replace(" ", "")
        answer_string = (
            answer_string.replace(",", "").replace(" ", "").replace(".", ",")
        )
    return answer_string if answer_string[-1] != "," else answer_string[:-1]


def append_question(
    the_source, the_metadata, the_question, the_answers, the_answer_index, the_comment
):
    # metadata[1] - question user_guess
    # metadata[2] - picture user_guess (higher than 0)
    the_file = open(the_source["full_file_path"], "a", encoding="utf-8")
    the_file.write(
        f"{the_metadata[0]}{the_metadata[1]}{the_metadata[0]}{the_metadata[2]}{the_metadata[0]}\n"
    )
    the_file.write(the_question)
    the_file.write(f"{the_metadata[0]}{len(the_answers)}")
    for zy_answer in the_answers:
        the_file.write(f"{the_metadata[0]}{zy_answer}")
    the_file.write(f"{the_metadata[0]}{fix_format_multianswer(the_answer_index)}")
    the_file.write(f"{the_metadata[0]}{the_comment}\n")


def get_all_valid_folders():
    return sorted(
        [
            f.path
            for f in scandir(path.abspath(getcwd()))
            if f.is_dir()
            if f.name != ".idea"
            if f.name != ".git"
            if f.name != ".ignore"
            if f.name != ".venv"
            if f.name != "_debug"
            if f.name != "__pycache__"
        ]
    )
