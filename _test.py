import _test_data
import _creatorv2
import _types
import _chem


def test(val1, val2):
    assert val1 == val2, f"\n---Expected: \n{val2} \n---got: \n{val1}"


def _answers(task: _types.TaskV2) -> list[str]:
    """Get answers from task."""
    return task.get_answers()


def _do_test():
    # --------------- Answers
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
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [x for x in range(121, 133 + 1)])
    # --------------- Questions
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
    test(
        questions[39].question,
        "Nurodykite, kuris junginys vaizduoja aziridino jono, kuris susidaro veikiant azoto mustardams, struktūrą.",
    )
    # --------------- Tasks (question + answer)
    converter = _creatorv2.get_answer_converter(mode="AB")
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_low = tasks[0]
    test(len(tasks), 66)
    test(task_low.original_num, 1)
    test(task_low.option_type, "AB")
    test(
        task_low.choices[task_low.answers_num[0] - 1],
        "Nosies purškalas, tirpalas 1 mg/ml",
    )
    task_high = tasks[-1]
    test(task_high.original_num, 66)
    test(task_high.option_type, "AB")
    test(
        task_high.choices[task_high.answers_num[0] - 1], "Fenilacto rūgšties dariniams"
    )
    task_z = tasks[33]
    test(task_z.original_num, 34)
    test(
        task_z.choices[task_z.answers_num[0] - 1],
        "slopina bakterijų sienelės biosintezę per UDP-N-acetilgliukozamino enolpiruvil transferazę (MurA) alkilindamas cisteiną",
    )
    task_z = tasks[30]
    test(task_z.original_num, 31)
    test(
        task_z.choices[task_z.answers_num[0] - 1],
        "Nėra 9-keto grupės, o tretinio amino įterpimas į makrolidinio žiedo struktūrą, padidino vaisto atsparumą rūgštims",
    )
    task_z = tasks[52]
    test(task_z.choices[task_z.answers_num[0] - 1], "Lorazepamas")
    task_z = tasks[56]
    test(
        task_z.choices[task_z.answers_num[0] - 1],
        "Selektyviai slopina serotonino reabsorbciją",
    )

    # --------------- Answers
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
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [118])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), 10)
    test(questions[0].question_num, 1)
    test(questions[-1].question_num, 10)
    test(questions[0].question, "Kurie iš šių teiginių apie resveratrolį yra teisingi?")
    test(
        questions[-1].question,
        "Kurio augalo preparatai tradiciškai vartojami kaip diuretikai?",
    )
    question_z = questions[1]
    test(question_z.question_num, 2)
    test(
        question_z.question,
        "Kokie yra mėlynių vaisių ekstrakto poveikiai?",
    )
    question_z = questions[2]
    test(question_z.question_num, 3)
    test(
        question_z.question,
        "Kokie yra žaliosios arbatos ekstrakto poveikiai diabeto komplikacijoms?",
    )
    question_z = questions[3]
    test(question_z.question_num, 4)
    test(
        question_z.question,
        "Kurie iš šių vaistinių augalų slopina TRH ir TTH aktyvumą?",
    )
    # --------------- Tasks (question + answer)

    converter = _creatorv2.get_answer_converter(
        mode="MULTI", conversions=_test_data.conversion2
    )
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_low = tasks[0]
    test(len(tasks), 10)
    test(task_low.original_num, 1)
    test(task_low.option_type, "MULTI")
    test(
        # [task_low.choices[answer_num - 1] for answer_num in task_low.answers_num],
        _answers(task_low),
        [
            "Slopina gliukoneogenezę ir gliukozės sintezę kepenyse.",
            "Aktyvina glikogeno sintezę.",
            "Apsaugo kasos β ląsteles nuo pažaidų ir apoptozės.",
        ],
    )
    task_high = tasks[-1]
    test(task_high.original_num, 10)
    test(task_high.option_type, "MULTI")
    test(_answers(task_high), ["Taraxacum officinale"])
    task_z = tasks[2]
    test(task_z.original_num, 3)
    test(
        _answers(task_z),
        [
            "Sumažina vibracinį jutimo slenkstį.",
            "Sumažina malondialdehido kiekį kraujyje.",
        ],
    )
    task_z = tasks[7]
    test(task_z.original_num, 8)
    test(_answers(task_z), ["Ūminis bronchitas", "Ūminis sinusitas"])
    task_z = tasks[8]
    test(task_z.original_num, 9)
    test(
        _answers(task_z),
        [
            "Kvapiųjų rozmarinų eterinis aliejus",
            "Vynuogių sėklų proantocianidinai",
            "Žaliosios arbatos katechinai",
            "Moliūgų fitosteroliai.",
        ],
    )

    # --------------- Answers
    body = _test_data.body3
    answers = _creatorv2.get_answers(body)
    answer_low = answers[0]
    answer_high = answers[-1]
    answers_num = [answer.question_num for answer in answers]
    test(answers_num, [x for x in range(1, 16)])
    test(answer_low.question_num, 1)
    test(answer_high.question_num, 15)
    test(answer_low.answer, "C")
    test(answer_high.answer, "B")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), 15)
    test(questions[0].question_num, 1)
    test(questions[-1].question_num, 15)
    test(
        questions[0].question,
        "Žinomiausias antikos laikų gydytojas.",
    )
    test(
        questions[-1].question,
        "Nepriklausomoje Lietuvos Respublikoje (1918-1940) buvo leidžiama steigti vaistines gavus Sveikatos departamento leidimą. Vaistinių skaičius buvo:",
    )
    test(
        questions[6].question,
        "Materia medica XVIII a. farmakopėjose buvo skirstoms į šias grupes:",
    )
    # --------------- Tasks (question + answer)
    converter = _creatorv2.get_answer_converter(mode="AB")
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_low = tasks[0]
    test(len(tasks), 15)
    test(task_low.original_num, 1)
    test(task_low.option_type, "AB")
    test(
        task_low.choices[task_low.answers_num[0] - 1],
        "Hipokratas.",
    )
    task_high = tasks[-1]
    test(task_high.original_num, 15)
    test(task_high.option_type, "AB")
    test(
        task_high.choices[task_high.answers_num[0] - 1],
        "Priklausė nuo gyventojų skaičiaus.",
    )

    # --------------- Pages
    pages = _creatorv2._get_pages(_test_data.body4)
    test([page.page_num for page in pages], [4, 5])

    # --------------- Answers
    body = _test_data.body5
    answers = _creatorv2.get_answers(body)
    _len = 8
    answer_low = answers[0]
    answer_high = answers[-1]
    answers_num = [answer.question_num for answer in answers]
    test(answers_num, [x for x in range(1, _len + 1)])
    test(answer_low.question_num, 1)
    test(answer_high.question_num, _len)
    test(answer_low.answer, "A")
    test(answer_high.answer, "E")
    answer_z = answers[6]
    test(answer_z.question_num, 7)
    test(answer_z.answer, "F")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [x for x in range(4, 6 + 1)])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), _len)
    test(questions[0].question_num, 1)
    test(questions[-1].question_num, _len)
    test(
        questions[0].question,
        "Pirmoji farmacininkų profesinė organizacija Vilniaus medicinos draugijos Farmacijos skyrius įkurtas 1819 m. Kuo rūpinosi ši organizacija?",
    )
    # --------------- Tasks (question + answer)

    # --------------- Answers
    body = _test_data.body6
    answers = _creatorv2.get_answers(body, lowest_num=69)
    answer_high = answers[-1]
    test(len(answers), 2)
    test(answer_high.question_num, 70)
    test(answer_high.answer, "E")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [29])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), 2)
    test(questions[-1].question_num, 70)
    test(
        questions[-1].question,
        "Kurios farmacinės substancijos, pasižyminčios rūgštinėmis savybėmis, negalima tiesiogiai nutitruoti NaOH:",
    )
    converter = _creatorv2.get_answer_converter(mode="AB")
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_high = tasks[-1]
    test(len(tasks), 2)
    test(task_high.original_num, 70)
    test(task_high.option_type, "AB")
    test(
        task_high.choices[task_high.answers_num[0] - 1],
        "H3BO3",
    )

    # --------------- Answers
    body = _test_data.body7
    answers = _creatorv2.get_answers(body)
    count = 15
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "B")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [30, 31])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Kurie iš pateiktų teiginių apie chloramfenikolį yra neteisingi:",
    )
    converter = _creatorv2.get_answer_converter(
        mode="MULTI", conversions=_test_data.conversion2
    )
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_high = tasks[-1]
    test(len(tasks), count)
    test(task_high.original_num, count)
    test(task_high.option_type, "MULTI")
    test(
        _answers(task_high),
        [
            "Jo molekulėje yra fenolinė ir alkoholinė hidroksilo grupės",
            "Abu jo molekulėje esantys N atomai pasižymi bazinėmis savybėmis",
        ],
    )

    # --------------- Answers
    body = _test_data.body8
    answers = _creatorv2.get_answers(body)
    count = 20
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "B")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [43, 45])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Kaip išsidėsto PAM emulsiklio molekulės emulsijose?",
    )
    converter = _creatorv2.get_answer_converter(
        mode="MULTI", conversions=_test_data.conversion2
    )
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_high = tasks[-1]
    test(len(tasks), count)
    test(task_high.original_num, count)
    test(task_high.option_type, "MULTI")
    test(
        _answers(task_high),
        [
            "Hidrofilinės emulsiklio molekulių dalys panirusios į vandeninę emulsijos fazę",
            "Hidrofobinės emulsiklio molekulių dalys pasiskirsčiusios aliejinėje fazėje",
        ],
    )

    # --------------- Answers
    body = _test_data.body9
    answers = _creatorv2.get_answers(body)
    count = 67
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "A")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [49, 50, 51, 52, 53, 54, 55, 56])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Preparatų nuo jūros ligos gamybai naudojamas:",
    )
    converter = _creatorv2.get_answer_converter(
        mode="AB", conversions=_test_data.conversion2
    )
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_high = tasks[-1]
    test(len(tasks), count)
    test(task_high.original_num, count)
    test(task_high.option_type, "AB")
    test(
        _answers(task_high),
        ["Skopolaminas"],
    )

    # --------------- Answers
    body = _test_data.body10
    answers = _creatorv2.get_answers(body)
    count = 66
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "C")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [64, 65, 66, 67, 68, 69, 70, 71])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    question_z = questions[8]
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Hipertiroidizmas gali būti gydomas:",
    )
    test(
        question_z.question,
        "Koks nepageidaujamos reakcijos virškinimo traktui dažnis, jeigu iš 10000 klinikiniame tyrime dalyvavusių pacientų 20-iai nustatytas su vaisto vartojimu susijęs viduriavimas?",
    )
    converter = _creatorv2.get_answer_converter(
        mode="AB", conversions=_test_data.conversion2
    )
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_high = tasks[-1]
    test(len(tasks), count)
    test(task_high.original_num, count)
    test(task_high.option_type, "AB")
    test(
        _answers(task_high),
        ["Metimazolu"],
    )

    # --------------- chems
    body = """
    NH4+, Hg2+
    A) H2C2O4·2H2O, PO43-
    """
    chems = _chem.get_chems_partial(body)
    test(len(chems), 5)
    test(
        [x.chem_unscripted for x in chems], ["NH4+", "Hg2+", "H2C2O4", "2H2O", "PO43-"]
    )
    chems = _chem.get_chems_full(chems)
    test([x.chem for x in chems], ["NH₄⁺", "Hg²⁺", "H₂C₂O₄", "2H₂O", "PO₄³⁻"])

    print("All tests passed.")


if __name__ == "__main__":
    _do_test()
