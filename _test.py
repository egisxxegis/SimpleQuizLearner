import _test_data
import _creatorv2


def test(val1, val2):
    assert val1 == val2, f"Expected {val2} \nbut got {val1}"


def _do_test():
    body = _test_data.body1
    answers = _creatorv2.get_answers(body)
    answer_low = answers[0]
    answer_high = answers[-1]
    answers_num = [answer.question_num for answer in answers]
    test(answers_num, [x for x in range(1, 67)])
    test(answer_low.question_num, 1)
    test(answer_high.question_num, 66)
    test(answer_low.answer, "A")
    test(answer_high.answer, "B")
    # ---------------
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), 66)
    test(questions[0].question_num, 1)
    test(questions[-1].question_num, 66)
    test(
        questions[0].question,
        "Kokia farmacine forma (ir stiprumu) vartojamas Ksilometazolinas?",
    )
    test(
        questions[-1].question,
        "Kuriai grupei pagal cheminę struktūrą yra priskiriamas pavaizduotas NVNU?",
    )
    # ---------------
    body = _test_data.body2
    answers = _creatorv2.get_answers(body)
    answer_low = answers[0]
    answer_high = answers[-1]
    answers_num = [answer.question_num for answer in answers]
    test(answers_num, [x for x in range(1, 11)])
    test(answer_low.question_num, 1)
    test(answer_high.question_num, 10)
    test(answer_low.answer, "A")
    test(answer_high.answer, "D")
    # ---------------
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), 10)
    test(questions[0].question_num, 1)
    test(questions[-1].question_num, 10)
    test(questions[0].question, "Kurie iš šių teiginių apie resveratrolį yra teisingi?")
    test(
        questions[-1].question,
        "Kurio augalo preparatai tradiciškai vartojami kaip diuretikai?",
    )

    print("All tests passed.")


if __name__ == "__main__":
    _do_test()
