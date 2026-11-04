import io, re

P = r'C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb'
p = P + r'\TASK_TRACKER.md'
t = io.open(p, encoding='utf-8').read()
L = t.split('\n')

# ---------------- 1. rewrite the four item rows with the measured facts ----------------
NEW = {
 'A7': '| A7 | P0 | 004 T9 | "Nothing but pads on J1 pins 16 to 20; firmware map agrees." | New | '
        '**Settled by measurement 2026-11-02** - Aswin metered the microSD slot: pin 2 to GPIO10, '
        'pin 3 to GPIO11, pin 5 to GPIO12, pin 7 to GPIO13, pin 4 to 3V3, pin 6 to GND, **nothing on GPIO9**. '
        'So CHK-001 C11 is right about GPIO10-13 and wrong to include GPIO14, and `/I2C0_SCL` on GPIO9 is safe. '
        'The violation stands: J1.16 carries `/E22_M1` (GPIO10) and J1.17 carries `/E22_M0` (GPIO11) - the card\'s '
        'CS and MOSI. T-55 straps both mode pins to ground and frees them | pad nets; Aswin\'s continuity '
        'measurement 2026-11-02; Ebyte E22-900T22D manual section 3 | T-02, T-55 |',
 'C2': '| C2 | P0 | 004 T9 | "24-hour run; no corruption after 20 power cuts." | New | '
        'The conflict is now measured, not contested: the slot owns GPIO10-13, so it is unusable while '
        '`/E22_M0`/`/E22_M1` sit on GPIO11/GPIO10. T-55 removes that; the 24-hour run is still not planned '
        'and no reading exists | Aswin\'s measurement 2026-11-02; CHK-001 C11 | T-23, T-55 |',
 'C5': '| C5 | P1 | 004 T9 | "Firmware reads back channel, address, power and key." | Partly | '
        'M0 and M1 are on separate pins as the item requires, but until T-55 they sit on the microSD\'s '
        'CS and MOSI. With both strapped to ground through 0 ohm the read-back is still possible over UART '
        '(AUX and the two UART lines are unaffected) and the card is free. '
        '**Note: strapping to ground removes hardware mode control in circuit** - configuration mode is '
        'reached by lifting one 0 ohm strap, which is reachable with the module out of its socket '
        '| Aswin\'s measurement 2026-11-02; Ebyte manual sections 6.2-6.5 | T-23, T-55 |',
 'R11': '| R11 | P1 | 001 T13 | "Pin map (C13); bench counts that match a reference at 1, 10 and 50 Hz." | New | '
        'The reed is on GPIO41, which CHK-001 C11 lists as output-only (GPIO40-42 are the board\'s LEDs). '
        '**A usable destination is now identified**: J2.9 = GPIO39 is unconnected on our board, and it is the '
        'only free input in that block - GPIO35-38 are the octal-PSRAM group the N16R8 module owns, and '
        'GPIO40 is also LED-only. T-56 moves `/REED_PULSE_F` from J2.7 to J2.9 '
        '| pad nets; Aswin\'s measurement of J2 pad names 2026-11-02; CHK-001 C11 | T-23, T-56 |',
}
done = []
for i, l in enumerate(L):
    m = re.match(r'^\|\s*(A7|C2|C5|R11)\s*\|\s*P', l)
    if m and m.group(1) not in done:
        L[i] = NEW[m.group(1)]
        done.append(m.group(1))
print('rows rewritten:', done)

# ---------------- 2. renumber the duplicated findings 22-25 (second set) to 26-29 ----------------
fixes = [
 ('22. **The E22 antenna keep-out area is crossed by two B.Cu tracks',
  '26. **The E22 antenna keep-out area is crossed by two B.Cu tracks'),
 ('23. **The J6 rewire is a reroute, not a net rename',
  '27. **SUPERSEDED - J6 is NOT mis-wired.** Finding 23 of this run read'),
 ('24. **Two of the five module outlines were on the wrong sockets',
  '28. **Two of the five module outlines were on the wrong sockets'),
 ('25. **The J6 pin-1 confirmation does not exist in the workspace',
  '29. **The J6 pin-1 confirmation now exists - closed 2026-11-02.** It did not exist when'),
]
for a, b in fixes:
    hit = False
    for i, l in enumerate(L):
        if l.startswith(a) and not hit:
            L[i] = b + l[len(a):]
            hit = True
            break
    print('renumbered', a[:34], '->', hit)

t = '\n'.join(L)

# ---------------- 3. insert the new findings at the end of Part 6 (before Part 7) ----------------
FINDINGS = """30. **The LoRa socket is numbered for a 180-degree insertion, and nothing says so.**
    Found 2026-11-02, and it cost a day. Read against the Ebyte datasheet order
    (1 M0, 2 M1, 3 RXD, 4 TXD, 5 AUX, 6 VCC, 7 GND) with the module inserted the
    obvious way, J6 looked mirror-imaged - VCC on GPIO10, GND on GPIO11, 5 V on M1.
    Inserted the other way round, **all seven nets line up**, including UART
    direction, and it matches Aswin's working bench wiring exactly. The net names
    themselves (`/E22_M0` on pad 7, `/E22_M1` on pad 6) prove the designer intended
    it. The real defect is that **no silk marks the orientation, the footprint pads
    are named only 1 to 7, and the header is unkeyed** - so the wrong way is both
    possible and invisible. Item A3's acceptance is "a reversed module cannot go in
    or is obvious"; today it does neither. Evidence: `pcb\\MoriShield_Carrier.kicad_pcb`
    J6 pad nets; Ebyte E22-900T22D manual section 3; Aswin's continuity test on the
    module's GND pin against the SMA shell.

31. **The capacitance sensor is an FDC1004 on J21, which is I2C channel 5 - and J15
    is a separate analog soil input.** The schematic gives J21 the value `FDC1004`;
    J21 carries `/I2C0_SDA_CH5` and `/I2C0_SCL_CH5`. J15 is a 3-pin port carrying
    `/SOIL_ADC_RAW` through R29 and C34 into **GPIO2 = ADC1_CH1**. Both analog inputs
    (J15 on GPIO2, J16 on GPIO1) land on **ADC1**, which is the ADC that keeps working
    with Wi-Fi on - ADC2 (GPIO11-20) does not. That was luck, not a decision, and it is
    worth recording because it constrains any future pin swap. Consequence for the
    keep-out work: **CH5 is not spare**, it is the FDC1004.

32. **Port names are drawn on layers that never print.** Only nine board-level
    silkscreen items exist on F.SilkS: `5v +`, `5v -`, `MoriShield Carrier`, `Rev C`,
    `S/N`, two `1` pin-1 marks, `MODEM THIS WAY UP` and `Q1 buzzer`. Every port name
    (`J15 SOIL`, `J11 SGP41 0x59`, `J12 SHT45 0x44`, `J14 BME688 0x76`, `J13 SPS30 5V`,
    `GY-521`, `DS3231 RTC`, `J5 MODEM 5V`, `J18 +5V IN`) is on **F.Fab**, which is not
    in the Gerber set. A builder therefore sees no port labels at all. In the schematic
    the naming is inconsistent: J21 `FDC1004`, J23 `EXT_BTN`, J24 `PANEL_LED_5V` and
    J25 `BUZZER_5V` are named, while J7, J8, J11, J12, J13, J14, J15, J16, J17, J20,
    J21, J22 and J26 are generic `JST_XH_n` / `Sock_1xnn` values. Items E5 and C12 and
    the CTO's repeated complaint about labels all point here. Evidence: layer-by-layer
    text dump, 2026-11-02.

33. **Part 6 of this register had two findings numbered 22, 23, 24 and 25.** The
    2026-11-02 run appended its own set without checking the existing numbers. Fixed
    by renumbering the later set to 26-29. A register that cites "finding 23" is
    ambiguous until this is clean.

34. **J17 and J20 have no identified purpose anywhere in the workspace.** Both are
    wired 4-pin I2C channel ports (CH4 and CH6) with ESD arrays, pull-ups and full
    copper. J20 is one of the two runs blocking the LoRa antenna keep-out. Nothing in
    the schematic, the board, the CTO documents or the notes says what sensor goes
    there. Asking Aswin - see `REPLY_TO_CTO.md` question 10.
"""
rows = t.split('\n')
k = next(n for n, l in enumerate(rows) if l.startswith('## Part 7'))
block = FINDINGS.split('\n')
rows[k:k] = block + ['']
t = '\n'.join(rows)

# ---------------- 4. append the new tasks ----------------
i = next(n for n, l in enumerate(t.split('\n')) if l.startswith('## Part 6'))
rows = t.split('\n')
for n in range(i):
    if rows[n].startswith('| T-54 |'):
        rows.insert(n + 1, '| T-55 | **Strap E22 M0 and M1 to GND through two 0 ohm 0603 resistors** at J6, '
                            'delete nets `/E22_M0` and `/E22_M1`, and set J1.16 / J1.17 to '
                            'unconnected-(J1-IO10-Pad16) and unconnected-(J1-IO11-Pad17). Frees the microSD. '
                            'Record the lift-a-strap route to configuration mode in the assembly note | '
                            'A7, C2, C5, R11, C11 | DEV | M |')
        rows.insert(n + 2, '| T-56 | **Move `/REED_PULSE_F` from J2.7 (GPIO41, output-only) to J2.9 (GPIO39)**, '
                            'the only free usable input in that block. J2.7 becomes '
                            'unconnected-(J2-IO41-Pad7) | R11, C11, C4 | DEV | S |')
        rows.insert(n + 3, '| T-57 | **Label the ports where a builder will see them**: name every port in the '
                            'schematic Value field, copy the port names onto F.SilkS at 1.0 mm / 0.15 mm stroke, '
                            'and mark J6 with its pin functions and its orientation. Do not invent names for J17 '
                            'and J20 | E5, C12, A3, C11 | DEV | M |')
        rows.insert(n + 4, '| T-58 | **Ask for a keyed or shrouded header at J6** (and J3/J4) as a costed option. '
                            'Silk makes a reversed insertion obvious; only a key makes it impossible | A3, R16 | DOC | S |')
        break
t = '\n'.join(rows)

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('TASK_TRACKER written. lines:', len(t.split('\n')))
