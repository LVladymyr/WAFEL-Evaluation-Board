# Component Selection Justification: Power & Balancing Circuits

This document outlines the engineering calculations and reasoning behind the component choices for the high-power and cell balancing sections of the WAFEL EVAL BOARD.

## 1. Pre-Charge & Pre-Discharge Circuits

### The Resistors (R603, R604) - "The Shock Absorbers"
The pre-charge circuit safely fills the massive capacitive load of a motor controller before turning on the main power MOSFETs, preventing sparks and inrush current damage.
*   **Configuration:** Two 510Ω resistors in parallel (Equivalent resistance = 255Ω).
*   **Worst-Case Scenario (10S / 42V Battery):** At the instant the pre-charge MOSFET turns on into a dead short (empty capacitors), the full 42V drops across the resistors.
*   **Current:** `I = V / R = 42V / 255Ω = 0.164A (164mA)`
*   **Total Power Spike:** `P = V * I = 42V * 0.164A = 6.88 Watts`
*   **Power Per Resistor:** `6.88W / 2 = 3.44 Watts`

**Selection:** A tiny 0603 resistor would instantly vaporize under a 3.44W pulse. We specifically chose large pulse-withstanding SMD packages (like **1206** or **2512**) because they have the physical mass to absorb this short, massive heat spike (which typically lasts only 10-50 milliseconds) safely without failing. Using two resistors in parallel cuts the thermal stress on each component in half, making the circuit bulletproof.

### The MOSFETs (Q601, Q701) - "The Switches"
It may seem counterintuitive to pair massive power resistors with a relatively small P-Channel MOSFET like the **IRFR9024** (TO-252/DPAK), but the math proves it runs perfectly cold.
*   **Rds_on of IRFR9024:** ~0.175Ω
*   **Current flowing through MOSFET:** 0.164A (Same as the resistors, since they are in series)
*   **Heat generated in MOSFET:** `P = I² * R = (0.164A)² * 0.175Ω = 0.0047 Watts (4.7 mW)`

**Selection:** While the resistors must absorb nearly 7 Watts of heat, the MOSFET only dissipates a microscopic 4.7 milliWatts. A TO-252 package can passively dissipate 1.5 Watts in open air and handle 11 Amps continuously. It is completely overkill for this switching task, ensuring it will never overheat.

---

## 2. Cell Balancing (CB) Mosfet Cascades

### The Balancing Resistors (R1001, R1002)
When the BMS detects an overcharged cell, it turns on the balancing MOSFET to bleed off the excess energy as heat through the balancing resistors.
*   **Configuration:** Two 100Ω resistors in parallel per cell (Equivalent resistance = 50Ω).
*   **Maximum Cell Voltage:** 4.2V
*   **Balancing Current:** `I = V / R = 4.2V / 50Ω = 84 mA`
*   **Total Heat:** `P = V² / R = (4.2V)² / 50Ω = 0.352 Watts`
*   **Heat per Resistor:** `0.352W / 2 = 0.176 Watts`

**Selection:** A standard 0603 resistor is rated for a maximum of 0.100W, meaning it would overheat and fail at 0.176W. A standard 0805 is rated for 0.125W, which is still too small. Therefore, we **must use the 1206 package**, which is rated for 0.250W (1/4 Watt). This ensures the resistors can safely bleed off power for hours without thermally stressing the PCB. 
*(Note: R1004 is part of the high-impedance voltage sense line, drawing practically zero current, so it safely remains an 0603).*

### The Balancing MOSFETs (Q1001 Array)
Since the absolute maximum balancing current is only 84 mA, we do not need a large power MOSFET for this task.
*   **Original Choice:** DMG2302UK (SOT-23, rated for 4.2A) - Massive overkill and wastes board space.
*   **New Choice:** **CJ3134K**
*   **Package:** SOT-723 (1.20 x 1.20 mm)

**Selection:** The CJ3134K is rated for 20V and 750mA. This easily handles our 4.2V / 84mA requirement while taking up 60% less physical space on the PCB than an SOT-23 package. Because there are 10 of these circuits on the board (one for each cell), switching to the SOT-723 package reclaims a massive amount of layout space, allowing for a much denser and cleaner 100x64mm board design.