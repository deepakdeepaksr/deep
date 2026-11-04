"""Correct the hand-typed gate tally in the session reports to the counted one.

Counted from TASK_TRACKER Part 2 rows by _cto_extract\\gate_truth.py:
4 met (C1, C2, C5, C12), 1 partly (C9), 8 not met (C3, C4, C6, C7, C8, C10, C11, C13).
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(ROOT, "work done")
text = io.open(path, encoding="utf-8").read()

PAIRS = [
    ('Gate tally: **4 met (C1, C2, C5, C12), 2 partly (C9, C10), 7 not met.** `pack.ps1` stops at **GATE 5',
     'Gate tally, counted from the rows by `_cto_extract\\gate_truth.py`: **4 met (C1, C2, C5, C12), '
     '1 partly (C9), 8 not met (C3, C4, C6, C7, C8, C10, C11, C13).** (Corrected 2026-11-03: this report '
     'first repeated a hand-typed "2 partly (C9, C10), 7 not met", which contradicted C10\'s own row.) '
     '`pack.ps1` stops at **GATE 5'),
    ('4 met, 2 partly, 7 not met. `pack.ps1` stops at GATE 5 PRODUCTION.',
     '4 met, 1 partly (C9), 8 not met. `pack.ps1` stops at GATE 5 PRODUCTION.'),
]

for old, new in PAIRS:
    if old not in text:
        print("MISS:", old[:70])
        continue
    text = text.replace(old, new, 1)
    print("fixed:", old[:60])

io.open(path, "w", encoding="utf-8", newline="").write(text)
left = text.count("2 partly")
print("remaining '2 partly' occurrences:", left)
