from FileHandler import get_content
from os import path, scandir, getcwd
from random import randint, shuffle


def get_all_content():
    all_folders = [f.path for f in scandir(path.abspath(getcwd())) if f.is_dir()
                   if f.name != ".idea"
                   if f.name != ".git"
                   if f.name != "__pycache__"]
    all_content = []
    for folder in all_folders:
        the_path = path.join(folder, "questions.txt")
        source = {"full_file_path": the_path}
        the_content = get_content(source, "%!%")
        all_content += the_content

    return all_content


if __name__ == "__main__":
    content = get_all_content()

    i_range = [x for x in range(0, len(content))]
    shuffle(i_range)
    right = 0
    total = 0
    for i in i_range:
        # i = randint(0, len(content)-1)
        task = content[i]
        print("\n------------------------------------------------------------------")
        print(f"({i+1}/{len(content)}; your score: {right}/{total}) {task.question}")
        print(f"\n")
        answer_indexes = [0, 1, 2, 3]
        shuffle(answer_indexes)
        for ii in range(len(answer_indexes)):
            print(f"{ii+1}. {task.answers[answer_indexes[ii]]}")
        number = int(input("Your choice? - "))
        if answer_indexes[number-1] == task.answer_i:
            print("------Correct")
            right += 1
        else:
            print(f"------Incorrect. Right answer was {task.answer_i + 1}.")
            print(task.comment)
        total += 1

        input("\n-------Enter to continue\n")
