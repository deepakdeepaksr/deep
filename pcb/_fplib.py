# -*- coding: utf-8 -*-
# Extract a footprint block from the board by Reference, or list refs per content group.
import re, sys, hashlib, difflib

PCB = 'MoriShield_Carrier.kicad_pcb'
LIB = '..\\morishield\\morishield_hardware\\libraries\\MoriShield_Carrier.pretty\\'

def blocks(text):
    # yield (start_idx, end_idx, name) for each top-level (footprint "...") block
    for m in re.finditer(r'(?m)^\t\(footprint \"[^\"]+\"', text):
        s = m.start()
        nxt = text.find('\n\t)\n', s)
        e = nxt + 4 if nxt != -1 else len(text)
        yield s, e, m.group(0)

def ref_of(blk):
    m = re.search(r'\(property \"Reference\" \"([^\"]+)\"', blk)
    return m.group(1) if m else '?'

def get_block(text, ref):
    for s, e, h in blocks(text):
        blk = text[s:e]
        if ref_of(blk) == ref:
            return blk
    return None

def scrub(t):
    t = re.sub(r'[ \t]*\(path [^\n]*\n', '', t)
    t = re.sub(r'[ \t]*\(sheetname [^\n]*\n', '', t)
    t = re.sub(r'[ \t]*\(sheetfile [^\n]*\n', '', t)
    t = re.sub(r'\(uuid \"[^\"]+\"', '(uuid \"X\"', t)
    t = re.sub(r'\n[ \t]*\(net \"[^\"]*\"\)', '', t)
    t = re.sub(r'\(at [-\d.]+ [-\d.]+( [-\d.]+)?\)(\s*\n\s*\(descr)', r'(at N N)\2', t, count=1)
    t = re.sub(r'\"Reference\" \"[^\"]*\"', '\"Reference\" \"R\"', t)
    return t

if __name__ == '__main__':
    cmd = sys.argv[1]
    text = open(PCB, encoding='utf-8').read()
    if cmd == 'groups':
        g = {}
        for s, e, h in blocks(text):
            blk = text[s:e]
            g.setdefault(hashlib.md5(scrub(blk).encode()).hexdigest()[:8], []).append(ref_of(blk))
        for k, v in g.items():
            print(k, v)
    elif cmd == 'extract':
        ref, fpid, out, mode = sys.argv[2], sys.argv[3], sys.argv[4], (sys.argv[5] if len(sys.argv) > 5 else 'raw')
        blk = get_block(text, ref)
        assert blk, 'no block for ' + ref
        blk = re.sub(r'\(footprint \"[^\"]+\"', '(footprint \"%s\"' % fpid, blk, count=1)
        if 'at0' in mode:
            blk = re.sub(r'(\(uuid \"[^\"]+\"\)\s*\n\s*\(at) [-+\d.]+ [-+\d.]+( [-+\d.]+)?\)', r'\g<1> 0 0)', blk, count=1)
        if 'refval' in mode:
            blk = re.sub(r'\(property \"Reference\" \"[^\"]*\"', '(property \"Reference\" \"REF**\"', blk, count=1)
            blk = re.sub(r'\(property \"Value\" \"[^\"]*\"', '(property \"Value\" \"%s\"' % fpid.split(':')[-1], blk, count=1)
        if 'strip' in mode:
            blk = re.sub(r'[ \t]*\(path [^\n]*\n', '', blk)
            blk = re.sub(r'[ \t]*\(sheetname [^\n]*\n', '', blk)
            blk = re.sub(r'[ \t]*\(sheetfile [^\n]*\n', '', blk)
            blk = re.sub(r'\n[ \t]*\(net \"[^\"]*\"\)', '', blk)
        open(LIB + out, 'w', encoding='utf-8').write(blk)
        print('wrote', out, 'from', ref, 'mode', mode)
    elif cmd == 'diff':
        a, b = get_block(text, sys.argv[2]), get_block(text, sys.argv[3])
        for x in difflib.unified_diff(scrub(a).splitlines(), scrub(b).splitlines(), lineterm='', n=1):
            if x.startswith(('+', '-')) and not x.startswith(('+++', '---')):
                print(x)
