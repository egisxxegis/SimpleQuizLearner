from FileHandler import fix_format_multianswer


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
