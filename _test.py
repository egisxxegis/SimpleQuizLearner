import _test_data
import _creatorv2
import _types
import _chem
import _quizerv2
import FileHandler
import os


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
    # answers = _creatorv2.get_answers(body, lowest_num=69)
    answers = _creatorv2.get_answers(body)
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

    # --------------- Answers
    body = _test_data.body11
    answers = _creatorv2.get_answers(body)
    count = 17
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, 83)
    test(answer_high.answer, "B")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [74, 75, 76])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, 83)
    test(
        questions[-1].question,
        "Kurie teiginiai apie sulfanilamidus yra teisingi?",
    )
    converter = _creatorv2.get_answer_converter(
        mode="MULTI", conversions=_test_data.conversion2
    )
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_high = tasks[-1]
    test(len(tasks), count)
    test(task_high.original_num, 83)
    test(task_high.option_type, "MULTI")
    test(
        _answers(task_high),
        [
            "Gali sukelti hemolizę pacientams, turintiems gliukozės-6-fosfato nepakankamumą",
            "Naujagimiams gali sukelti kernicterus (naujagimių geltą)",
        ],
    )

    # --------------- Answers
    body = _test_data.body12
    answers = _creatorv2.get_answers(body)
    count = 12
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "A")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [102, 104])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    question_z = questions[9]
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Kokie BNP skaičiavimo metodai yra naudojami?",
    )
    test(
        question_z.question,
        "Kokios strategijos naudojamos produkto brandos stadijoje ?",
    )
    converter = _creatorv2.get_answer_converter(
        mode="MULTI", conversions=_test_data.conversion12
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
        ["Pajamų metodas", "Išlaidų metodas", "Gamybos metodas"],
    )
    task_z = tasks[9]
    test(task_z.original_num, 10)
    test(task_z.option_type, "MULTI")
    test(_answers(task_z), ["Rinkos modifikavimo.", "Prekės modifikavimo."])
    test(len(task_z.choices), 4)

    # --------------- Answers
    body = _test_data.body13
    answers = _creatorv2.get_answers(body)
    count = 46
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "B")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [141, 142, 143, 144])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Koks yra paracetamolio toksinio poveikio mechanizmas?",
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
        [
            "Perdozavus paracetamolio, išsenka glutationo atsargos – pažeidžiamos kepenys."
        ],
    )

    # --------------- Answers
    body = _test_data.body14
    answers = _creatorv2.get_answers(body)
    count = 56
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "B")
    # --------------- Pages
    # pages = _creatorv2._get_pages(body)
    # test([page.page_num for page in pages], [141, 142, 143, 144])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Vaistinėje 1 metus saugomi šie popieriniai receptai:",
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
        [
            "1 formos, pagal kuriuos parduoti vaistiniai preparatai, kurių veikliosios medžiagos bendrinis pavadinimas yra semagliutidas;"
        ],
    )

    # --------------- Answers
    body = _test_data.body15
    answers = _creatorv2.get_answers(body)
    count = 22
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "A")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [180, 181, 182, 183, 184, 185, 186])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Įmonės veiklos valdymas (operational management) apima šias sritis:",
    )
    converter = _creatorv2.get_answer_converter(
        mode="MULTI", conversions=_test_data.conversion2
    )
    tasks = _creatorv2.get_tasks(
        raw=body, questions=questions, answers=answers, answer_converter=converter
    )
    task_high = tasks[-1]
    task_z = tasks[14]
    test(len(tasks), count)
    test(task_high.original_num, count)
    test(task_high.option_type, "MULTI")
    test(
        _answers(task_high),
        [
            "Prekių ir paslaugų asortimento formavimas",
            "Įmonės procesų valdymas",
            "Kokybės valdymas",
        ],
    )
    test(task_z.original_num, 15)
    test(task_z.option_type, "MULTI")
    test(
        _answers(task_z),
        [
            "Vieta, skirta Geros vaistinių praktikos nuostatuose nustatytoms kitoms paslaugoms teikti",
            "Vieta, skirta vaistinių preparatų pakuotei perpakuoti, perfasuoti, pateikčiai keisti",
            "Vieta, kurioje priimami ir tvarkomi vaistiniai preparatai",
        ],
    )

    # --------------- Answers
    body = _test_data.body16
    answers = _creatorv2.get_answers(body)
    count = 22
    answer_high = answers[-1]
    test(len(answers), count)
    test(answer_high.question_num, count)
    test(answer_high.answer, "B")
    # --------------- Pages
    pages = _creatorv2._get_pages(body)
    test([page.page_num for page in pages], [188, 189, 190, 191])
    # --------------- Questions
    questions = _creatorv2.get_questions(body, answers)
    test(len(questions), count)
    test(questions[-1].question_num, count)
    test(
        questions[-1].question,
        "Prekės į kategorijas vaistinėse skirstomos, pagal tai kaip jos turi būti laikomos oficinoje. (LR SAM įsakymas V- 1849,2016.12.29)",
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
        ["Ne"],
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

    tasks_packed = [
        _quizerv2.get_tasks_v2(
            full_file_path=os.path.join(folder, "questions.json"), its_folder=folder
        )
        for folder in FileHandler.get_all_valid_folders()
    ]
    tasks: list[_types.TaskV2] = []
    for pack in tasks_packed:
        tasks.extend(pack)
    pictured_tasks = [task for task in tasks if task.random_picture_from is not None]

    # check ref: task --> image
    for task in pictured_tasks:
        for picture_path in task.random_picture_from:
            if not os.path.exists(picture_path):
                raise FileNotFoundError(f"Image not found: {picture_path}")
            if str(task.original_num) not in picture_path:
                raise ValueError(
                    f"Image {picture_path} does not match task number {task.original_num}."
                )

    # check ref: image --> task
    folders = FileHandler.get_all_valid_folders()
    for folder in folders:
        pictures: list[tuple[str, str]] = []
        for file in os.scandir(folder):
            if file.is_file() and file.name.lower().split(".")[-1] in [
                "jpg",
                "png",
                "gif",
                "jpeg",
                "webp",
                "bmp",
            ]:
                pictures.append((file.name, file.path))
        tasks = _quizerv2.get_tasks_v2(
            full_file_path=os.path.join(folder, "questions.json"), its_folder=folder
        )
        _pictured_tasks = [
            task for task in tasks if task.random_picture_from is not None
        ]
        for picture_name, picture_path in pictures:
            found = False
            for task in _pictured_tasks:
                if picture_path in task.random_picture_from:
                    found = True
                    break
            if not found:
                raise ValueError(
                    f"Image {picture_name} does not match any task in folder {folder}."
                )

    # check shuffle-imaged tasks have no text
    for task in pictured_tasks:
        if len(task.random_picture_from) > 1:
            assert [x.strip() for x in task.choices] == [
                "" for _ in task.choices
            ], f"Task {task.number=} has text but multiple images. Text: {task.question}"

    # intify
    test(_creatorv2._intify_multis(["1", "A", "2"])[0], [1, "A", 2])
    test(
        _creatorv2._intify_multis(
            ["1", "*", "2", "-"],
        ),
        ([1, "*", 2, "-"], "*"),
    )
    test(
        _creatorv2._intify_multis(["1", "A", "2", "B"], ["B", "a", "1", 2])[0],
        [3, 2, 4, 1],
    )
    test(
        _creatorv2._intify_multis(
            ["2", "A", "D"], [1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]
        )[0],
        [2, 10, 13],
    )

    # parse
    test(_creatorv2._parse_multis("145ab*-c", 1, 9, "a", "c"), None)
    test(
        _creatorv2._parse_multis("145abc", 1, 9, "a", "c"),
        ["1", "4", "5", "a", "b", "c"],
    )
    test(
        _creatorv2._parse_multis("9,14,5,abc145abc", 1, 9, "a", "c"),
        ["1", "4", "5", "9", "a", "b", "c"],
    )

    # folder indexes
    test(
        _quizerv2.get_folder_indexes(
            "13;,.,;,/,;'a", [1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 3
        ),
        [0, 1, 2, 6, 7, 8, 27, 28, 29],
    )

    # only for pharm stuff. comment me if not the case.
    if True:
        test(len(tasks_packed) % 3, 0)

    # multichoice or abc. pick only one
    if True:
        for pack in tasks_packed:
            _type = pack[0].option_type
            for task in pack:
                if task.option_type != _type:
                    raise ValueError(
                        f"Task {task.original_num} mixed type: {task.option_type} != {_type}. Question text: {task.question}"
                    )

    # you are abc but demand multi? Redflag
    if True:
        for task in tasks:
            if task.option_type != "MULTI" and len(task.answers_num) > 1:
                raise ValueError(
                    f"Task {task.original_num} is not MULTI but has multiple answers: {task.answers_num}. Question text: {task.question}"
                )

    # folder order
    if True:
        test(folders[0].split("p")[-1], "001_004")
        test(folders[-1].split("p")[-1], "246_246")
        test(len(folders), 63)
        folders2 = sorted(folders.copy())
        test(folders, folders2)

    print("All tests passed.")


if __name__ == "__main__":
    _do_test()
