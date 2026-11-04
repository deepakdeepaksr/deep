Here's everything on your plate, in the order that unblocks the most. Nothing here needs the carrier board — it isn't manufactured yet, so I've separated what you can do **today** from what has to wait for first boards.

---

# PART A — Today, no tools. About 30 minutes.

## A1. Send Serigreen this message · *10 min*

This is the highest-value thing you can do today, because their answers gate everything Devin and I can't decide. Copy it, cut what you disagree with, send on your usual channel.

```
Subject: MoriShield Carrier Rev C - nine questions that stop work

Rev C package is in progress. These nine are blocking. One line each is enough.

1. RS485 (item C1, P0). Do you accept a written deferral for this revision?
   Reason: the wind sensor is now a reed switch plus an AS5600 magnetic encoder,
   and the soil probe is read on demand by a setup engineer's laptop through a
   USB-RS485 adapter - it is not a board-mounted continuous interface.

2. J18 input protection (item R4, P0). Do you accept a discrete over-voltage and
   reverse-polarity controller driving low-Rds FETs, in place of the TPS26630 you
   named? Our arithmetic: 40 m ohm against your 60 m ohm board allocation with the
   discrete route, 66 m ohm with the TPS26630's 31 m ohm internal switch.

3. Converter (condition 1). You are the component supplier, so we are not buying
   one. Condition 1 asks for an input rating of 40 V or more. Every module we can
   buy here is 36-38 V operating. Note also that any TVS able to stand off the
   22-25 V battery disconnect clamps around 39-42 V - so the clause and the surge
   part fight each other. Please either supply a converter meeting the clause, or
   sign the deviation and tell us which half you are trading.

4. Antenna keep-out (item E3). We have the LoRa module's SMA position. We need the
   ESP32 board's on-board antenna end confirmed from your side too, and the modem's
   U.FL position. We will not draw a keep-out over a guess.

5. Vias in SMD pads (item R16, check C5). 67 of 319 vias sit inside an SMD pad. We
   propose one fab note - plug, fill and cap per IPC-4761 Class B or C - rather
   than 67 routing changes. Do you agree, and can you price it? Hand assembly makes
   this close to mandatory: an unfilled via under a pad wicks solder away.

6. Keyed headers (item A3). J6, J3 and J4 are unkeyed. We have added silkscreen so
   a reversed module is obvious, but only a key makes it impossible. Do you want a
   shrouded or keyed header specified, and at what cost limit?

7. E22 supply rail. The board feeds the LoRa module from 5 V. Its TXD and AUX
   outputs are TTL and follow the supply, and the ESP32-S3 is not 5 V tolerant. We
   propose moving the module to 3.3 V, which is how we tested it. Any objection?

8. Sensor channels 4 and 6 (ports J17 and J20). Both are fully wired I2C channel
   ports with ESD arrays and pull-ups. Nothing in 003, 004 or our notes says which
   sensor goes there. One of them sits in the corridor we need for the LoRa
   antenna keep-out.

9. Correction to CHK-001 C11, with the measurement behind it. C11 says "GPIO10 to 14
   are the board's own microSD". We metered the slot on the board you supply:
   GPIO10, 11, 12 and 13 - CS, MOSI, CLK, MISO - and GPIO14 is not on the slot,
   nor is GPIO9. Please confirm, so we can stop reserving a pin we do not need to.

For information, no action needed:
- The microSD conflict is closed. E22 M0 and M1 are now strapped to ground through
  0 ohm resistors, which frees GPIO10 and GPIO11 for the card.
- The reed switch has moved off GPIO41 to GPIO39.
- Ground stitching (E1) is met: 148 links, worst 10.00 mm, 0.0% beyond 10 mm.
```

## A2. Tell the firmware side one sentence · *2 min*

> **When an E22 is put into configuration mode, it only speaks 9600 8N1** — the Ebyte manual, section 7.1. If firmware opens the port at a different rate, the module looks dead.

This matters because configuration on this board means **removing strap resistor R56** with the module lifted off its socket. Whoever does that at assembly needs the baud rate set first.

## A3. Decide one thing · *5 min*

**Do you want the microSD slot to work?**

- **Yes** → nothing to do. GPIO10–13 belong to the card and stay unused by us. That's the current design.
- **No** → tell me, and we can reclaim GPIO12 and GPIO13 for something else. GPIO10 and 11 stay unusable either way because the card wiring is inside the EdgeHax board, not on our carrier.

Say which and I'll note it in the register so nobody re-litigates it.

## A4. Answer from memory, no tools · *5 min*

**What goes on J17 (channel 4) and J20 (channel 6)?** Both are wired and ready. If you don't know, say "unknown" and question 8 above stands.

---

# PART B — Today, with calipers. About 20 minutes.

You need: **digital calipers**, a **ruler or tape**, your **phone**, and the four modules on the table — the EdgeHax ESP32 board, the Parry modem board, the GY-521, the DS3231.

## B1. The ESP32 antenna tab — the number that unblocks a keep-out · *5 min*

**Why:** our ESP32 outline stops 2.5 mm past the header row, but the antenna sticks out much further. Until we know how much further, we can't draw the copper-free zone or trust the 3D box check.

1. Put the **EdgeHax S3-PRO** flat on the table, USB end toward you, unpowered.
2. Look at the **far end** — the end away from the USB socket. You're looking for a **zig-zag copper line**, like a squiggly snake drawn on the board, usually with a row of small round pads along the very edge.
3. **Measure 1:** from the **outermost tip of that copper** (the very edge of the board) to the **centre of the nearest header hole** on either row. Hold the caliper flat against the board and read it.
4. **Measure 2:** how far the zig-zag extends **sideways** — its width across the board.
5. **Photograph:** the antenna end close up, with a ruler lying along the board showing the number.

Write it as: `antenna tip to nearest header hole centre = ___ mm` and `antenna width = ___ mm`.

## B2. The modem's U.FL position · *4 min*

**Why:** the antenna connector is on the **underside** of the modem board, so it lives in the gap between the modem and the carrier. We need to know exactly where in that gap, because that decides whether a pigtail can be fitted at all, and where the hole in the box goes.

1. Turn the **Parry modem board** over so you see the **underside** (the side that faces the carrier when plugged in).
2. Find the **U.FL connector** — a small round silver disc, roughly **6–7 mm across**, with a thin metal ring around its edge. It looks like a tiny button.
3. **Measure 1:** from the **centre of that disc** to the **nearest edge of the board**, in mm.
4. **Measure 2:** from the centre of the disc to the **nearest header pin hole**.
5. **Measure 3:** the disc's **height above the board** — caliper jaws flat on the board, closing on the underside of the connector. It's usually about 2 mm.
6. Photograph the underside with a ruler beside it.

## B3. How tall the socket plastic is — the number that decides everything under a module · *3 min*

**Why:** this is the clearance between the carrier and the underside of any plugged-in module. Everything we've argued about — the U.FL, J5, "is anything crushed" — comes down to this one number.

1. Take **one empty female header strip** (the socket that will be soldered to the carrier — a 1×12 or 1×22, whichever you have).
2. Stand it on its **open end** (the end the module's pins go in from the top).
3. Measure from the **table** to the **top of the plastic**.
4. That is the gap. Standard parts are usually **9.0–9.5 mm**. Write the real number.
5. Then measure the **pin length** too — how far the pins stick out of the bottom. Subtract: **gap − pin protrusion = the actual clearance** under the module.

Write: `socket plastic height = ___ mm, pin protrudes ___ mm below, so usable gap = ___ mm`.

## B4. GY-521 and DS3231 heights — the two numbers marked TBC · *4 min*

**Why:** the 3D check needs every module's height, and these two are still `TBC` in the documents. Devin can't measure what it can't see.

**GY-521 (the accelerometer):**
1. Stand it on its **back**, chip side up.
2. Measure from the **bottom of the PCB** to the **tallest point**. On this board that's usually the **pin headers sticking up** if they're not cut short, or the chip itself.
3. Measure it **both ways**: pins fitted, and pins cut flat. Note which you plan to use.

**DS3231 (the RTC):**
1. Stand it on its **back**.
2. The **round coin-cell battery holder** is the tallest part — measure from the PCB's bottom to the **top of the battery**.
3. Also measure the **diameter** of the battery, because it overhangs the board edge and affects whether it clears anything underneath.

Write: `GY-521 height = ___ mm (pins fitted / cut)`, `DS3231 height = ___ mm`, `DS3231 battery diameter = ___ mm`.

## B5. The J5 terminal block — height and which side the wire leaves · *4 min*

**Why:** J5 moved to (222.00, 91.40), and we calculated only **1.91 mm of room on one side and 5.1 mm on the other** for the wire to bend. That's a physical reality, not a drawing.

1. Pick up the **MX126 terminal block** — the 2-pin screw terminal with **5.0 mm spacing**, the same part that's on J5 and J18.
2. **Measure its total height** from the PCB mounting surface to the top.
3. **Look at where the wire enters** — the opening for the wire. Is it on the **top face**, or on the **front edge** (the side facing away from the board)?
4. **Measure the wire-entry opening's distance** from the edge of the plastic body.
5. **Check the screwdriver**: hold one at the angle you'd naturally approach from, over the terminal. Does your hand hit anything 4 mm away?

Then answer this in words: **"the wire leaves the terminal from the ___ side, and I need ___ mm of clear space there."**

Write: `MX126 height = ___ mm, wire entry = top / side, clear space needed = ___ mm`.

---

# PART C — Not today. These need the carrier built.

I want to be blunt about this so nobody wastes time hunting for results that physically cannot exist yet. **The carrier PCB is not manufactured.** So these cannot be done:

| Item | What it needs | When |
|---|---|---|
| **B10** — the modem burst voltage trace | A built carrier, the modem, a 5 V supply and a scope | After first boards |
| **C2** — 24-hour run and 20 power-cycles | A built carrier with the ESP32 board | After first boards |
| **R11** — reed counts against a reference at 1, 10, 50 Hz | A built carrier | After first boards |
| **A2** — modem registering on the network | A built carrier, SIM, coverage | After first boards |
| **Test-fit** of J5 under the modem, J26 under the RTC | A built carrier | After first boards — **but the 3D check we're building now is the substitute** |

**What you do today in Part B is what makes those items shorter later.** Every measurement above feeds the 3D model so the first board doesn't come back with a crushed connector.

---

# PART D — Housekeeping while Devin works · *2 min*

1. **Do not open `pcb\MoriShield_Carrier.kicad_pcb` or `.kicad_sch` in KiCad while Devin is working.** If you open it and save, your save overwrites his work — no warning, no merge. If you want to look, open a copy from `pcb\_snap\`.
2. **Let OneDrive finish syncing** before you copy anything to the new laptop. The folder is large and partial sync gives you placeholder files that look fine and read as errors.
3. **Copy the whole `new pcb` folder**, not selected files. These must travel together:
   - `pcb\` — including `pcb\_snap\` (that's your undo history)
   - `morishield\morishield_hardware\libraries\` — **the footprint library. If it doesn't come, the schematic opens with 124 errors.**
   - `revC\`, `_cto_extract\`
   - The four root documents: `PROJECT_CONTEXT_RevC.md`, `TASK_TRACKER.md`, `STAGE_TRACKER.md`, `REPLY_TO_CTO.md`
   - `ESP32_S3_WROOM_N16R8_Pinout_Reference.md`, `a7672s_4g_lte_modem_pinout_guide.md`
4. **On the new laptop:** install KiCad **10.0** at `C:\Program Files\KiCad\10.0`. Scripts hard-code that path. And 95 files contain the old workspace path — either recreate the same folder path exactly, or tell me and I'll do one pass replacing them.

---

# Fill this in and send it back

```
B1  ESP32 antenna tip to nearest header hole centre : ______ mm
    antenna width across the board                 : ______ mm
    photo                                          : yes / no

B2  modem U.FL centre to nearest board edge        : ______ mm
    U.FL centre to nearest header hole             : ______ mm
    U.FL height above the board                    : ______ mm

B3  socket plastic height                          : ______ mm
    pin protrusion below the plastic               : ______ mm
    usable gap                                     : ______ mm

B4  GY-521 height (pins fitted / cut)              : ______ / ______ mm
    DS3231 height                                  : ______ mm
    DS3231 battery diameter                        : ______ mm

B5  MX126 terminal height                          : ______ mm
    wire entry                                     : top / side
    clear space needed at the wire entry           : ______ mm

A3  microSD slot: keep it working / don't care     : ______
A4  what goes on J17                               : ______
    what goes on J20                               : ______
A1  Serigreen message sent                        : yes / no, and on what date
```

**What each one unlocks:**

| Your number | What it lets us finish |
|---|---|
| B1 | ESP32 antenna keep-out → **E3 and check C10**, and the outline correction |
| B2 | Modem antenna keep-out → the second half of **E3** |
| B3 | The 3D clearance check → **check C9** and item **A4** |
| B4 | Removes the last two `TBC` heights → **C9** |
| B5 | Decides whether J5's new position is actually workable → **C9** |
| A4 | Whether the LoRa keep-out corridor can be freed → **C10** |
| A1 | Everything gated on Serigreen: **R4, condition 1, R16, C1** |

**Do A1 first.** It costs ten minutes and it's the only item on the list where the clock is someone else's.