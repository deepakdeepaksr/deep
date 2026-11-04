"""Extract text from the LM2596 datasheet PDF and grep the rating tables."""
import io
import re
import sys

from pypdf import PdfReader

SRC = r"C:\Users\aswin\.qoder\cache\projects\new pcb-1898cd80\agent-tools\b51e9830\90ad2f40.txt"
OUT = r"_cto_extract\LM2596_datasheet.txt"

r = PdfReader(SRC)
parts = []
for i, p in enumerate(r.pages):
    try:
        parts.append("\n=== PAGE %d ===\n" % (i + 1) + (p.extract_text() or ""))
    except Exception as e:
        parts.append("\n=== PAGE %d ===\n[fail %s]" % (i + 1, e))
txt = "".join(parts)
io.open(OUT, "w", encoding="utf-8").write(txt)
sys.stdout.write("pages=%d chars=%d\n" % (len(r.pages), len(txt)))
