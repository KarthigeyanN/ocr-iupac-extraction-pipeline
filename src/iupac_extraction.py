import re
from typing import List, Optional


IUPAC_HINTS = [
    "meth",
    "eth",
    "prop",
    "but",
    "pent",
    "hex",
    "hept",
    "oct",
    "non",
    "dec",
    "benz",
    "phen",
    "ol",
    "one",
    "amine",
    "amide",
    "acid",
]


def tokenize(text: str) -> List[str]:
    # Very simple tokenization by whitespace and punctuation
    tokens = re.findall(r"[A-Za-z0-9,\-\(\)]+", text)
    return tokens


def looks_like_iupac(token: str) -> bool:
    token_lower = token.lower()
    if len(token_lower) < 4:
        return False
    if not re.search(r"[a-zA-Z]", token_lower):
        return False
    return any(hint in token_lower for hint in IUPAC_HINTS)


def extract_iupac(text: str) -> Optional[str]:
    """
    Extract the most likely IUPAC-like token from text.
    For now, returns the first candidate.
    """
    tokens = tokenize(text)
    candidates = [t for t in tokens if looks_like_iupac(t)]

    if not candidates:
        return None

    # Simple heuristic: longest candidate
    candidates.sort(key=len, reverse=True)
    return candidates[0]
