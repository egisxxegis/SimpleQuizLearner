from FileHandler import *
from Quizer import *
from Creator import *
from Task import *


def pretty_print_yes_no(title, boolean_result):
    print("Testing: " + title)
    outcome = "Success" if boolean_result else "----------------------------------- Failed"
    print(f'{outcome}\n---------------')
    return not boolean_result


if __name__ == '__main__':

    error = False

    if not error:
        the_answers_in = "True1;True2;True3;False1;False2"
        the_answers_real = "True1;True2;True3;False1;False2".split(";")
        the_options = [";"]
        the_answers_out = extract_answers(the_answers_in, the_options, end_splitting=True)
        error = pretty_print_yes_no("Extract case x;x with [';']", the_answers_real == the_answers_out)

    if not error:
        the_answers_in = "True1;True2;True3;False1;False2"
        the_answers_real = "True1;True2;True3;False1;False2".split(";")
        the_options = [";", ";", ";", ";", ";"]
        the_answers_out = extract_answers(the_answers_in, the_options, end_splitting=True)
        error = pretty_print_yes_no("Extract case x;x", the_answers_real == the_answers_out)

    if not error:
        the_answers_in = "True1;True2;True3;False1;False2;"
        the_answers_real = "True1;True2;True3;False1;False2".split(";")
        the_options = [";", ";", ";", ";", ";"]
        the_answers_out = extract_answers(the_answers_in, the_options, end_splitting=True)
        error = pretty_print_yes_no("Extract case x;x;", the_answers_real == the_answers_out)

    if not error:
        the_answers_in = "a. True1\nb. True2\nc. True3\nd. False1\ne. False2"
        the_answers_real = "True1;True2;True3;False1;False2".split(";")
        the_options = ["a", "\nb", "\nc", "\nd", "\ne", '\nf']
        the_answers_out = extract_answers(the_answers_in, the_options, splitter_suffix='. ', end_splitting=False)
        error = pretty_print_yes_no("Extract case a. x b. x", the_answers_real == the_answers_out)
