import os
import re
from typing import Literal

from _creatorv2 import P_UN_LETTER_NUM, _re_finditer_overlapping
import _types


PATH_FOLDER = "_debug"
PATH_IN = os.path.join(PATH_FOLDER, "_chem_in.txt")
PATH_OUT = os.path.join(PATH_FOLDER, "_chem_out.txt")


def get_chems_partial(raw: str):
    """
    NH4+, Hg2+
    A) H2C2O4·2H2O,
    """
    pattern_element = r"[0-9]*[A-Z][a-z]?[0-9]*[\+\-]*"
    pattern = P_UN_LETTER_NUM + f"({pattern_element})+" + P_UN_LETTER_NUM
    findings = _re_finditer_overlapping(pattern, raw)
    chems: list[_types.SimpleChem] = []
    for finding in findings:
        if re.match(r"\s*[A-F][\.\–\)\s*]", finding.group(0)) or re.match(
            r"\s*CYP[0-9]{3}\s*", finding.group(0)
        ):
            continue
        chem_unscripted = finding.group(0)[1:-1]
        elements = re.findall(f"({pattern_element})", chem_unscripted)
        chems.append(
            _types.SimpleChem(
                raw=finding.group(0),
                chem_unscripted=chem_unscripted,
                elements_unscripted=elements,
                chem="a",
                chem_in_raw=raw,
            )
        )
    return chems


def superscript(num_or_polarity: int | Literal["-", "+"]) -> str:
    num_or_polarity = str(num_or_polarity)
    mapping = {
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
        "+": "⁺",
        "-": "⁻",
    }
    if num_or_polarity in mapping:
        return mapping[num_or_polarity]
    raise ValueError(
        f"{num_or_polarity} is not a valid superscript value. Values: {mapping.keys()}"
    )


def subscript(num: int | str) -> str:
    num = str(num)
    mapping = {
        "1": "₁",
        "2": "₂",
        "3": "₃",
        "4": "₄",
        "5": "₅",
        "6": "₆",
        "7": "₇",
        "8": "₈",
        "9": "₉",
    }
    if num in mapping:
        return mapping[num]
    raise ValueError(f"{num} is not a valid subscript value. Values: {mapping.keys()}")


def get_chem_full(chem: _types.SimpleChem) -> _types.SimpleChem:
    get_body = lambda el: re.search(r"([A-Z][a-z]*)", el).group(1)

    def supersub(unprefixed_el: str) -> str:
        body = get_body(unprefixed_el)
        el_parts = unprefixed_el.split(body)
        prefix = el_parts[0]
        suffix = el_parts[-1]
        if not suffix:
            return unprefixed_el
        shall_superscript = False
        if suffix[-1] in ["+", "-"]:
            shall_superscript = True
        supers = []
        parts = [symbol for symbol in suffix]
        while len(parts) > 0 and shall_superscript:
            part = parts.pop()
            part_is_num = part not in ["+", "-"]
            if len(chem.elements_unscripted) > 1 and part_is_num:
                # take 1/2 numbers, but not 1/1 numbers
                if len(parts) == 0 or str(supers[-1]).isnumeric():
                    # sorry, undo 1/1
                    parts.append(part)
                    break
            #  Cr3+ jonų oksidacijai becomes Cr³⁺
            supers.append(part)
            if part_is_num:
                break  # taking only one number
        supers.reverse()
        subs = parts
        return "".join(
            [prefix, body]
            + [subscript(x) for x in subs]
            + [superscript(x) for x in supers]
        )

    chem_str = "".join([supersub(el) for el in chem.elements_unscripted])
    return _types.SimpleChem(
        raw=chem.raw,
        chem_unscripted=chem.chem_unscripted,
        elements_unscripted=chem.elements_unscripted,
        chem=chem_str,
        chem_in_raw=chem.raw[0] + chem_str + chem.raw[-1],
    )


def get_chems_full(chems: list[_types.SimpleChem]) -> list[_types.SimpleChem]:
    return [get_chem_full(chem) for chem in chems]


def process_chem_file():
    with open(PATH_IN, "r", encoding="utf-8") as file:
        raw = file.read()
    chems = get_chems_partial(raw)
    chems = get_chems_full(chems)
    for chem in chems:
        raw = raw.replace(chem.raw, chem.chem_in_raw, 1)
    with open(PATH_OUT, "w", encoding="utf-8") as file:
        file.write(raw)
    print(f"Processed {len(chems)} chems. See {PATH_OUT}")


if __name__ == "__main__":
    process_chem_file()
    pass
