import json, collections, re, os

base = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'


def dump(path, label):
    p = os.path.join(base, '_cto_extract', path)
    d = json.load(open(p, encoding='utf-8'))
    print('=' * 70)
    print(label, ' date:', d.get('date'), ' source:', os.path.basename(d.get('source', '')))
    if 'ignored_checks' in d:
        print('  ignored checks:', [i.get('key') for i in d['ignored_checks']])
    if 'sheets' in d:                                   # ERC
        sev = collections.Counter()
        typ = collections.Counter()
        msgs = collections.defaultdict(list)
        for s in d['sheets']:
            for v in s.get('violations', []):
                sev[v.get('severity')] += 1
                typ[v.get('type')] += 1
                dsc = (v.get('items') or [{}])[0].get('description', '')
                if len(msgs[v.get('type')]) < 3:
                    msgs[v.get('type')].append(dsc[:110])
        print('  ERC violations by severity:', dict(sev))
        print('  ERC by type:')
        for t, n in typ.most_common():
            print('    %-42s %4d   e.g. %s' % (t, n, msgs[t][0] if msgs[t] else ''))
    if 'violations' in d:                                # DRC
        sev = collections.Counter(v.get('severity') for v in d['violations'])
        typ = collections.Counter(v.get('type') for v in d['violations'])
        print('  DRC violations by severity:', dict(sev))
        print('  DRC by type:')
        for t, n in typ.most_common(20):
            ex = ''
            for v in d['violations']:
                if v.get('type') == t:
                    its = v.get('items') or []
                    if its:
                        ex = (its[0].get('description') or '')[:90]
                        if ex:
                            break
            print('    %-42s %4d   %s' % (t, n, ex))
        unc = d.get('unconnected_items', [])
        print('  UNCONNECTED items:', len(unc))
        for u in unc[:12]:
            its = u.get('items') or []
            print('    ', u.get('type'), '|', (its[0].get('description') if its else '')[:100])
        par = d.get('schematic_parity', [])
        pt = collections.Counter(p.get('type') for p in par)
        print('  SCHEMATIC PARITY:', len(par), dict(pt))
        shown = collections.Counter()
        for p in par:
            t = p.get('type')
            if shown[t] < 4:
                shown[t] += 1
                its = p.get('items') or []
                print('    %-38s %s' % (t, (its[0].get('description') if its else '')[:110]))


dump('erc_pcb.json', 'ERC  pcb\\MoriShield_Carrier.kicad_sch')
dump('drc_pcb.json', 'DRC  pcb\\MoriShield_Carrier.kicad_pcb')
