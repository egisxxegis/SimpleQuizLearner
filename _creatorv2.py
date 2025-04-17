import os
import json
import re
from typing import Literal

import _types

P_UNPREFIXED = r"[^0-9a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ#\.\-–\?\:\=]"
P_UN_LETTER_NUM = r"[^0-9a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ]"


def _assert_deltas(nums: list[int], place: str):
    if len(nums) > 2:
        deltas = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
        assert deltas == [1] * (
            len(nums) - 1
        ), f"bad deltas at {place}. {nums=} {deltas=}"


def _re_finditer_overlapping(pattern, string: str, flags=0):
    matches: list[re.Match[str]] = []
    haystack = string
    start_i_to_boost = {}
    while True:
        found = re.search(pattern, haystack, flags)
        if found:
            if not found.group().startswith("#"):
                matches.append(found)
            _start = found.start() + 1
            boost = start_i_to_boost.get(_start, 0)
            start_i = _start + boost
            start_i_to_boost[_start] = boost + 1
            haystack = "#" * (start_i) + haystack[start_i:]
            if found.start() == len(string) - 1:
                break
        else:
            break
    return matches


def get_answers(raw: str, lowest_num: int = 1):
    """
    59 – D
    60 – D
    133

    6 – C
    7 – D
    """
    pattern_num = r"\d+"
    pattern_answer = (
        r"[abcdefABCDEF]+"  # supplying '+' to prevent parsing '4. Define' as '4. D'
    )
    pattern_separator = r"[.\-–:]?"
    pattern = r"\s*".join(
        ["(", pattern_num, pattern_separator, pattern_separator, pattern_answer, ")"]
    )
    findings: list[str] = re.findall(pattern, raw)
    answers: list[_types.SimpleAnswer] = []
    for finding in findings:
        num = re.search(pattern_num, finding).group()
        answer = re.search(pattern_answer, finding).group()
        try:
            answers.append(
                _types.SimpleAnswer(
                    raw=finding, answer=answer.upper(), question_num=int(num)
                )
            )
        except ValueError:
            pass

    # possibly some noise from questions and from pagination.
    # thus search for sequence [1; x] in the end
    # 144 6 5 2 143 1 4 3 1
    # ---> 6 5 4 3 2 1
    answers_reverse = answers[::-1]
    num_to_answer = dict()
    for answer in answers_reverse:
        if answer.question_num not in num_to_answer:
            num_to_answer[answer.question_num] = answer
        else:
            pass  # discarded

    is_edited = True
    while is_edited:
        is_edited = False
        nums = list(num_to_answer.keys())
        nums.sort(reverse=True)
        for num in nums:
            if num == lowest_num:
                continue
            if num < lowest_num or num - 1 not in num_to_answer:
                num_to_answer.pop(num)
                is_edited = True

    values: list[_types.SimpleAnswer] = list(num_to_answer.values())
    values = sorted(values, key=lambda x: x.question_num)
    _assert_deltas([x.question_num for x in values], "get_answers")
    return values


def _cut_answers(raw: str, answers: list[_types.SimpleAnswer]):
    assert len(answers) >= 2, "Not enough answers to parse questions."
    pattern_answers_start = (
        re.escape(answers[0].raw) + r".{0,11}?" + re.escape(answers[1].raw)
    )
    parts = re.split(pattern_answers_start, raw, 1, re.DOTALL)
    assert len(parts) == 2, "Cannot split questions and answers."
    pattern = r"[^\n]{0,20}atsak.{1,10}$"
    body = re.split(pattern, parts[0], 0, re.IGNORECASE)[0]
    return body


def _get_pages(raw: str):
    """

    130


    """
    linear_space = r"[\t\f\v ]"
    pattern = r"\n" + linear_space + r"*([0-9]+)" + linear_space + r"+\n"
    pages: list[_types.SimplePage] = []
    for found in _re_finditer_overlapping(pattern, raw):
        page = _types.SimplePage(raw=found.group(0), page_num=int(found.group(1)))
        pages.append(page)
    _assert_deltas([x.page_num for x in pages], "get_pages")

    return pages


def _remove_pages(raw: str):
    pages = _get_pages(raw)
    for page in pages:
        raw = raw.replace(page.raw, "\n")
    return raw


def get_questions(raw: str, answers: list[_types.SimpleAnswer]):
    body = "\n\n " + _remove_pages(_cut_answers(raw, answers))

    """
    2. Kokie yra mėlynių vaisių ekstrakto poveikiai? 
    1. Antioksidacinis. 
    2. Priešuždegiminis. 
    3. Hipoglikeminis. 
    4. Lipidų metabolizmą reguliuojantis.
    """
    questions: list[_types.SimpleQuestion] = []
    for big_num in sorted([answer.question_num for answer in answers], reverse=True):
        pattern = (
            r"\s{2}" + rf"({big_num}\s?\." + r".{5,}?\s*\n\s*" + r")[Aa1]\s*[\.\-–\)]"
        )
        findings = [
            found for found in _re_finditer_overlapping(pattern, body, re.DOTALL)
        ]
        if len(findings) == 0:
            raise ValueError(f"Cant find question {big_num}.")
        qsearch = findings[-1]  # for AB
        for finding in findings[::-1]:
            _pattern = P_UNPREFIXED + f"{big_num+1}" + r"\s*[\.\-–\)]"
            if re.search(
                _pattern,
                finding.group(1),
            ):
                # question 2. starts with option 3. ? suspicious
                continue
            else:
                qsearch = finding
                break

        # qsearch = [found for found in re.finditer(pattern, body, re.DOTALL)][-1]
        assert qsearch, big_num
        body = body[: qsearch.start()]
        question = _types.SimpleQuestion(
            raw=qsearch.group(1),
            question_num=big_num,
            question=re.sub(
                f"{big_num}" + r"\s*[.\-–:]", "", qsearch.group(1), 1, re.DOTALL
            )
            .replace("\n", "")
            .replace("\r", "")
            .strip("\t "),
        )
        questions.append(question)
    questions = questions[::-1]
    _assert_deltas([x.question_num for x in questions], "get_questions")
    return questions


def check_tasks_well_scanned(_raw: str, tasks: list[_types.SimpleTask]):
    tasks = sorted(tasks, key=lambda x: x.question.question_num)
    raw = _remove_pages(_cut_answers(_raw, [task.answer for task in tasks]))
    raw_sub = raw

    make_pattern = (
        lambda _items: r"\s*"
        + r"\s*?".join([re.escape(str(item).strip()) for item in _items])
        + r"\s*?"
    )

    errors = []
    iterative_error_str = (
        "Iterative tasks not well scanned. See _debug folder for comparison."
    )

    items: list[str] = []
    for task in tasks:
        task_items: list[str] = []
        task_items.append(task.question.raw)
        for option in task.options:
            task_items.append(option.raw)
        items.extend(task_items)
        if iterative_error_str in errors:
            continue
        pattern = make_pattern(task_items)
        found = re.search(pattern, raw_sub, re.DOTALL)
        if not found or found.start() != 0:
            with open("_debug/_sub_clipboard.txt", "w", encoding="utf-8") as f_sub:
                with open("_debug/_sub_pattern.txt", "w", encoding="utf-8") as f_pat:
                    with open("_debug/_sub_raw.txt", "w", encoding="utf-8") as f_raw:
                        f_sub.write(raw_sub)
                        f_pat.write(pattern)
                        f_raw.write("\n".join(task_items))
            errors.append(iterative_error_str)
            continue
        raw_sub = raw_sub[found.end(0) :]
    raw2 = "\n".join(items + ["\n"])
    pattern = make_pattern(items)
    if not re.match(pattern, raw, re.DOTALL):
        if not os.path.exists("_debug"):
            os.mkdir("_debug")
        with open("_debug/_clipboard.txt", "w", encoding="utf-8") as f_org:
            with open("_debug/_derived.txt", "w", encoding="utf-8") as f_new:
                f_org.write(raw)
                f_new.write(raw2)
        errors.append("Tasks not well scanned. See _debug folder for comparison.")

    if len(errors) > 0:
        raise ValueError("\n".join(errors))


def get_tasks(
    raw: str,
    questions: list[_types.SimpleQuestion],
    answers: list[_types.SimpleAnswer],
    answer_converter: _types.TypeAnswerConverter,
):
    """
        A) Valpro rūgšties analogams
    B) Feniltriazinams
    C) γ-aminosviesto rūgšties (GABA) analogams
    D) Benzodiazepinams
    """
    _raw = raw
    raw = _remove_pages(_cut_answers(_raw, answers))
    tasks: list[_types.TaskV2] = []
    tasks_simple: list[_types.SimpleTask] = []
    for question_high in questions[::-1]:
        answer_high = [
            answer
            for answer in answers
            if answer.question_num == question_high.question_num
        ][0]
        parts = raw.split(question_high.raw)
        assert len(parts) == 2, parts
        raw = parts[0]
        options_str = "\n" + parts[1] + "\n"
        p_id = r"[1-9a-fA-F]\s*[\.\-–\)]"
        p_base = r"\n\s*(" + f"{p_id}" + r")(.*?)"
        p_not_last = p_base + r"(\n\s*" + p_id + ")"
        p_last = p_base + "()$"
        options: list[_types.SimpleOption] = []
        while True:
            found1 = re.search(p_not_last, options_str, re.DOTALL)
            found2 = re.search(p_last, options_str, re.DOTALL)
            found = found1 or found2
            if not found:
                break
            options_str = options_str[found.end(2) :]
            option = _types.SimpleOption(
                raw=found.group(0).removesuffix(found.group(3)),
                option_id=found.group(1),
                option_num=0,
                option=found.group(2)
                .replace("\r", "")
                .replace("\n", "")
                .replace("\t", " ")
                .strip(" "),
            )
            options.append(option)
        for num, option in enumerate(options, 1):
            option.option_num = num
        assert (
            len(options) > 0
        ), f"Dead end at:\n{question_high.question_num}\n{question_high.question}"
        answers_i = answer_converter(answer_high.answer, len(options))
        tasks.append(
            _types.TaskV2(
                number=question_high.question_num,
                question=question_high.question,
                choices=[option.option for option in options],
                option_type=(
                    "MULTI" if re.search(r"[1-9]", options[0].option_id) else "AB"
                ),
                answers_num=answer_converter(answer_high.answer, len(options)),
                original_num=answer_high.question_num,
            )
        )
        tasks_simple.append(
            _types.SimpleTask(
                answer=answer_high, question=question_high, options=options
            )
        )
    tasks = sorted(tasks, key=lambda x: x.number)
    check_tasks_well_scanned(_raw, tasks_simple)
    return tasks


def ask_is_correct(can_be_empty: bool = False) -> bool:
    while True:
        prompt = "\n" if can_be_empty else "Is this correct? (Y/N)\n"
        is_correct = input(prompt)
        if can_be_empty and is_correct == "":
            return True
        if is_correct.upper() not in ["Y", "N"]:
            continue
        return is_correct.upper() == "Y"


def ask_mode() -> Literal["AB", "MULTI"]:
    while True:
        mode = input("Answer mode: AB or MULTI?\n")
        mode = mode.strip("\r\n\t ").upper()
        if mode in ["AB", "MULTI"]:
            return mode


def ask_letter_conversion(
    letter: _types.TypeAnswer, _converted: None | str = None
) -> _types.TypeAnswerConversion:
    while True:
        converted = _converted or input(
            f'Into which answer numbers the letter "{letter}" shall be converted?\n* is all\n- is not applicable\nExample: 1, 2, 6\n'
        )
        converted = converted.replace(" ", ",").replace(".", ",").replace(";", ",")
        # converted = re.sub(r",+", ",", converted)
        converted = converted.replace(",", "")
        values: list[int | str] = []
        # for value in converted.split(","):
        for value in converted:
            try:
                values.append(int(value))
            except ValueError:
                continue
        if converted.replace(",", "") in ["*", "-"]:
            converted = converted.replace(",", "")
            values = [converted]
        else:
            if len(values) < 0:
                print("No values scanned. Try again.")
                continue
            bad_values = [x for x in values if x < 1 or x > 6]
            if bad_values:
                print(
                    f"Some values are less than 1 or greater than 6. Try again. {bad_values}"
                )
                continue
        values = sorted(set(values))
        print(f"Understood as: {', '.join([str(x) for x in values])}")
        # is_correct = ask_is_correct(True) if _converted is None else True
        is_correct = True
        if is_correct:
            if converted == "*":
                return "all"
            elif converted == "-":
                return "N/A"
            else:
                return values


def ask_multi_converter(
    conversions: None | list[str] = None,
) -> _types.TypeAnswerConverter:
    letter_to_values: dict[_types.TypeAnswer, _types.TypeAnswerConversion] = {}
    is_autofill = False
    for i, letter in enumerate(_types.LETTERS):
        prefill = (
            None if conversions is None or len(conversions) <= i else conversions[i]
        )
        values: _types.TypeAnswerConversion = (
            "N/A" if is_autofill else ask_letter_conversion(letter, prefill)
        )
        letter_to_values[letter] = values
        if values == "N/A":
            is_autofill = True

    def derive_answers(letter: _types.TypeAnswer, options_count: int):
        values = letter_to_values[letter]
        if values == "N/A":
            raise ValueError(f"Letter {letter} is not applicable.")
        if values == "all":
            return [x for x in range(1, options_count + 1)]
        return values

    return derive_answers


def get_answer_converter(
    mode: None | Literal["AB", "MULTI"] = None, conversions: None | list[str] = None
) -> _types.TypeAnswerConverter:
    mode = mode or ask_mode()
    if mode == "AB":
        converter: _types.TypeAnswerConverter = lambda answer, options_count: [
            _types.LETTERS.index(str(answer).upper()) + 1
        ]
        return converter
    elif mode == "MULTI":
        return ask_multi_converter(conversions=conversions)


def get_are_tasks_correct(tasks: list[_types.TaskV2]) -> bool:
    for task in tasks:
        print(f"{task.number}. {task.question}")
        get_answer_id = lambda num: (
            f"{num}." if task.option_type == "MULTI" else f"{_types.LETTERS[num - 1]})"
        )
        for i, option in enumerate(task.choices, 1):
            _id = get_answer_id(i)
            print(f"{_id} {option}")
        print("\n")
        _id = ", ".join([str(get_answer_id(answer_i)) for answer_i in task.answers_num])
        print(f"Correct answer{'s' if len(task.answers_num)>1 else ''}: {_id}")
        if not ask_is_correct(True):
            return False
    return True


def collect_clipboard(initial_prompt: str, quit_command: str = "qq") -> str:
    body = input(initial_prompt)
    next_prompt = ""
    while True:
        raw = input(next_prompt)
        if next_prompt != "" and raw == quit_command:
            break
        if body.replace("\r", "").endswith("\n" * 7):
            next_prompt = f"To end data body, type: {quit_command}\n"
        body += "\n" + raw
    return body


def loop_create_one_folder():
    folder = input("Folder name: ")
    if os.path.exists(folder):
        print("Folder already exists. Bye")
    os.mkdir(folder)
    while True:
        answer_converter = get_answer_converter()
        raw = collect_clipboard(
            "Input full data with answer sheet.\n",
        )
        answers = get_answers(raw)
        questions = get_questions(raw, answers)
        tasks = get_tasks(raw, questions, answers, answer_converter)
        print(f"Found {len(questions)} questions")
        is_correct = ask_is_correct()
        if not is_correct:
            print("Restarting ...")
            continue
        print("Check the questions and answers.")
        if not get_are_tasks_correct(tasks):
            print("Restarting ...")
            continue
        print("Saving ...")
        with open(os.path.join(folder, "questions.json"), "w", encoding="utf-8") as f:
            json.dump(
                [task.model_dump() for task in tasks],
                f,
                ensure_ascii=False,
                indent=4,
            )
        print(f"Saved in folder {folder}")
        break


def loop_create():
    while True:
        loop_create_one_folder()
