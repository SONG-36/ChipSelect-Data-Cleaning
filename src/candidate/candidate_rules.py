# src/candidate/candidate_rules.py

import re
from typing import List, Dict

WINDOW = 80  # 上下文窗口大小（字符）

def _with_context(text: str, start: int, end: int, window: int = WINDOW) -> str:
    s = max(0, start - window)
    e = min(len(text), end + window)
    return text[s:e].replace("\n", " ")

def extract_candidates(text: str) -> List[Dict]:
    """
    Return a list of candidate dicts:
    { field, candidate, context }
    """
    candidates = []

    RULES = {
        "max_freq_mhz": re.compile(r"(\d{1,4})\s*mhz", re.IGNORECASE),
        "flash_kb": re.compile(r"(\d+(?:\.\d+)?)\s*(k|m)byte", re.IGNORECASE),
        "ram_kb": re.compile(r"(\d+(?:\.\d+)?)\s*(k|m)\s*byte", re.IGNORECASE),
        "vdd": re.compile(r"(\d\.\d)\s*v", re.IGNORECASE),
        "package": re.compile(r"\b(LQFP\d+|QFN\d+|BGA\d+)\b", re.IGNORECASE),
        "temp_grade": re.compile(r"(-\d+\s*(?:~|to)\s*\d+)\s*°?c", re.IGNORECASE),
    }

    for field, pattern in RULES.items():
        for m in pattern.finditer(text):
            cand = m.group(1)
            # 单位信息保留给 resolver，这里不做决策
            context = _with_context(text, m.start(), m.end())
            candidates.append({
                "field": field,
                "candidate": cand,
                "context": context
            })

    return candidates
