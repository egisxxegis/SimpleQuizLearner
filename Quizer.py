from FileHandler import get_content, get_all_valid_folders
from os import path
from random import shuffle


def get_all_content():
    all_folders = get_all_valid_folders()
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
        task = content[i]
        print("\n------------------------------------------------------------------")
        print(f"({i+1}/{len(content)}; your score: {right}/{total}) {task.question}")
        print(f"\n")
        answer_indexes = [0, 1, 2, 3]
        shuffle(answer_indexes)
        correct_index = 0
        for ii in range(len(answer_indexes)):
            print(f"{ii+1}. {task.answers[answer_indexes[ii]]}")
            if answer_indexes[ii] == task.answer_i:
                correct_index = ii+1
        number = int(input("Your choice? - "))
        if answer_indexes[number-1] == task.answer_i:
            print("------Correct")
            right += 1
        else:
            print(f"------Incorrect. Right answer was {correct_index}.")
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
