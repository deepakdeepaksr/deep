"""Extract text from the UMW LM2596 / LM2596HV datasheet PDF."""
import io
import sys

from pypdf import PdfReader

SRC = r"C:\Users\aswin\.qoder\cache\projects\new pcb-1898cd80\agent-tools\b51e9830\a98d4813.txt"
OUT = r"_cto_extract\LM2596HV_umw_datasheet.txt"

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
