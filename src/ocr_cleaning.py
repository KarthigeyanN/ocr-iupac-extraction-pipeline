import re
from typing import List


COMMON_OCR_CONFUSIONS = {
    "0": "O",
    "1": "l",
    "5": "S",
    "8": "B",
    "“": '"',
    "”": '"',
    "’": "'",
    "ﬁ": "fi",
    "ﬂ": "fl",
}


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00A0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fix_common_confusions(text: str) -> str:
    for wrong, right in COMMON_OCR_CONFUSIONS.items():
        text = text.replace(wrong, right)
    return text


def remove_hyphen_linebreaks(lines: List[str]) -> str:
    """
    Join lines where words are split by hyphen at line end:
    'N,N-dimethy-\ntryptamine' -> 'N,N-dimethyltryptamine'
    """
    joined = []
    buffer = ""

    for line in lines:
        line = line.rstrip("\n")
        if line.endswith("-"):
            buffer += line[:-1]
        else:
            buffer += line
            joined.append(buffer)
            buffer = ""

    if buffer:
        joined.append(buffer)

    return " ".join(joined)


def clean_ocr_text(raw_text: str) -> str:
    """
    High-level cleaning entrypoint.
    """
    lines = raw_text.splitlines()
    text = remove_hyphen_linebreaks(lines)
    text = fix_common_confusions(text)
    text = normalize_whitespace(text)
    return text
