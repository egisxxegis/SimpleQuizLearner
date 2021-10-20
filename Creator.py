from FileHandler import *


def exists_question(the_content: [Task], the_question):
    for the_task in the_content:
        if the_task.question.find(the_question) > -1:
            return True
    return False


def extract_answers(full_string: str, the_options: [str]):
    the_answers = []
    the_temp = full_string
    for the_i in range(len(the_options)):
        splitter = f'{the_options[the_i]}\n'
        splitter = '\n' + splitter if the_i != 0 else splitter
        the_temp = the_temp.split(splitter)

        if the_i != 0:
            the_answers.append(the_temp[0])

        the_temp = the_temp[1]
        the_i += 1
    the_answers.append(the_temp)
    return the_answers


if __name__ == "__main__":
    limiter = "%!%"
    part = str(input("What part do you want to create? (one part = 20 questions)"))
    source = {
        'folder': part,
        'full_file_path': f'{part}/questions.txt'
    }
    options = ['a.', 'b.', 'c.', 'd.']
    create_if_not_exists(source)
    while True:
        content = get_content(source, limiter)
        if len(content) == 20:
            print("---------------*********** Limit 20 questions reached. Stopping")
            break
        question = input("Input a part or full question.\n")
        if exists_question(content, question):
            print("------------Question exists. skipping")
        else:
            question = input("+++++++++++++++++++ Question is new. Type full question")
            picture_filename = input("+++++++++++++++++++ Picture number (not count) (>0)?")
            answers_raw = input("+++++++++++++++++++ Copy paste all answers.")
            answers = extract_answers(answers_raw, options)
            correct_answer_i = int(input(f"Which answer is correct of these {len(options)}?"))
            comment = input("What is comment?")
            append_question(source, [limiter, len(content)+1, picture_filename],
                            question, answers, correct_answer_i - 1, comment)
            print("+++++++++++++++++++++++++++++++ New Question added " +
                  f'({len(content) + 1 }/20)')


else:
    print('yellow')
