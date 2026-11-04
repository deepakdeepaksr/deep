"""Extract text from the XL4015 datasheet PDF fetched into the tool cache."""
import io
import re
import sys

from pypdf import PdfReader

SRC = r"C:\Users\aswin\.qoder\cache\projects\new pcb-1898cd80\agent-tools\b51e9830\4c46e51a.txt"
OUT = r"_cto_extract\XL4015_datasheet.txt"

r = PdfReader(SRC)
print("pages:", len(r.pages))
buf = io.StringIO()
for i, p in enumerate(r.pages):
    buf.write("\n=== PAGE %d ===\n" % (i + 1))
    try:
        buf.write(p.extract_text() or "")
    except Exception as e:
        buf.write("[extract failed: %s]" % e)
txt = buf.getvalue()
io.open(OUT, "w", encoding="utf-8").write(txt)
print("chars:", len(txt))
