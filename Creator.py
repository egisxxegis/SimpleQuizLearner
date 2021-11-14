from FileHandler import *
import shutil


def exists_question(the_content: [Task], the_question):
    for the_task in the_content:
        if the_task.question.find(the_question) > -1:
            return True
    return False


def extract_answers(full_string: str, the_options: [str], newline_in_splitter=True):
    the_answers = []
    the_temp = full_string
    the_suffix = '\n' if newline_in_splitter else ''
    for the_i in range(len(the_options)):
        splitter = f'{the_options[the_i]}{the_suffix}'
        splitter = '\n' + splitter if the_i != 0 else splitter
        the_temp = the_temp.split(splitter)

        if the_i != 0:
            the_answers.append(the_temp[0])

        if len(the_temp) > 1:
            the_temp = the_temp[1]
        else:
            return the_answers

    the_answers.append(the_temp)
    return the_answers


if __name__ == "__main__":
    limiter = "%!%"

    # do we need to move questions to ignore list
    while True:
        part = str(input("What part do you want to create? \n"
                         " *(one part = 20 questions)\n"
                         " *(type \".ignore\" to move old questions to ignore list)"))
        if part == ".ignore":
            for folder in get_all_valid_folders():
                shutil.move(folder, ".ignore")
            print("Moving has been attempted. No checks for errors done. Do it yourself")
            continue
        break

    source = {
        'folder': part,
        'full_file_path': f'{part}/questions.txt'
    }
    options = ['a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.']
    create_if_not_exists(source)
    while True:
        content = get_content(source, limiter)
        if len(content) == 20:
            print("---------------*********** Limit 20 questions reached. Stopping")
            break
        question = input("Input full question.\n")
        if exists_question(content, question):
            print("------------Question exists. skipping")
        else:
            print("+++++++++++++++++++ Question is new.")
            picture_filename = input("+++++++++++++++++++ Has a picture? NO = 0, YES = anything")
            if picture_filename != '0':
                picture_filename = str(len(content) + 1) + ".png"
                print(f"--************-------- Save image in {source['folder']} as a {picture_filename}")
                input("+++ press enter")
            answers_raw = input("+++++++++++++++++++ Copy paste all answers.")
            answers = extract_answers(answers_raw, options, newline_in_splitter=False)
            correct_answer_i = input(f"Which answer(s) is(are) correct of these {len(answers)}?")
            comment = input("What is comment?")
            append_question(source, [limiter, len(content)+1, picture_filename],
                            question, answers, correct_answer_i, comment)
            print("+++++++++++++++++++++++++++++++ New Question added " +
                  f'({len(content) + 1 }/20)')


else:
    print('yellow')
