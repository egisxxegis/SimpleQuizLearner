from os import path, mkdir
from Task import Task


def create_if_not_exists(the_source):
    if not path.exists(the_source['folder']):
        mkdir(the_source['folder'])
    if not path.exists(the_source['full_file_path']):
        open(the_source['full_file_path'], "x")


def get_content(the_source, the_limiter):
    the_file = open(the_source['full_file_path'], "r", encoding='utf-8')
    the_raw_content = the_file.read()
    the_content = []
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
            if the_picture_path != '0':
                the_task.set_picture(the_picture_path)
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
            the_task.answer_i = int(fragment)
        elif the_i == 6:
            the_task.comment = fragment

        the_i += 1
        if the_i == 7:
            the_content.append(the_task)
            the_i = 0
    return the_content


def exists_question(the_content: [Task], the_question):
    for the_task in the_content:
        if the_task.question.find(the_question) > -1:
            return True
    return False


def append_question(the_source, the_metadata, the_question, the_answers, the_answer_index, the_comment):
    # metadata[1] - question number
    # metadata[2] - picture number (higher than 0)
    the_file = open(the_source['full_file_path'], "a", encoding='utf-8')
    the_file.write(f'{the_metadata[0]}{the_metadata[1]}{the_metadata[0]}{the_metadata[2]}{the_metadata[0]}\n')
    the_file.write(the_question)
    the_file.write(f'{the_metadata[0]}{len(the_answers)}')
    for zy_answer in the_answers:
        the_file.write(f'{the_metadata[0]}{zy_answer}')
    the_file.write(f'{the_metadata[0]}{the_answer_index}')
    the_file.write(f'{the_metadata[0]}{the_comment}\n')


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
