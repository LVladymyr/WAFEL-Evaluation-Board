# WAFEL_EVAL_BOARD Budget Estimate

Based on live pricing data from JLCPCB and standard supplier costs for the major components of the battery management/eval board.

### Main ICs and Active Components
| Component | Ref | Qty | Unit Price | Total | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BQ7694204** (Battery Monitor) | U201 | 1 | $2.60 | $2.60 | *Live JLCPCB price (LCSC: C3038665)* |
| **NUCLEO-L432KC** (MCU) | U801 | 1 | ~$15.00 | $15.00 | *External (ST module), typically not assembled by JLC* |
| **IPB085N15NM6** (150V MOSFET) | Q401-Q503 | 6 | ~$2.00 | $12.00 | *Estimated Mouser/Digikey or JLC equivalent* |
| **LM5163DDAR** (Buck Converter) | U102 | 1 | $1.09 | $1.09 | *Live JLCPCB price (LCSC: C2873264)* |
| **TJA1051T/3** (CAN Transceiver) | U802 | 1 | $0.60 | $0.60 | *Live JLCPCB price (LCSC: C38695)* |
| **TPS70933DBVR** (LDO Regulator) | U101 | 1 | $0.16 | $0.16 | *Live JLCPCB price (LCSC: C89347)* |

### Passives & Protection
| Component | Ref | Qty | Unit Price | Total | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **10uH / 68uH Inductors** | L101, L102 | 2 | $0.18 | $0.36 | *Live JLCPCB price (LCSC: C2894721)* |
| **25A SMD Fuse** | F101 | 1 | $0.28 | $0.28 | *Live JLCPCB price (LCSC: C178980)* |
| **Misc SMD Passives** (R, C) | Various | ~150 | ~$0.01 | ~$1.50 | *Basic JLC parts are fractions of a cent* |
| **Diodes / Small FETs** | Various | ~15 | ~$0.05 | ~$0.75 | *TVS, Schottky, 2N7002, etc.* |

### PCB Fabrication & Assembly (JLCPCB)
*   **Bare PCBs (5 pcs):** ~$2.00 (Standard 2-layer, 100x100mm promo).
*   **SMT Assembly Setup (Engineering Fee):** ~$8.00 (Base fee for a single prototype run).
*   **Extended Component Fees:** JLC charges a $3 fee per "Extended" reel loaded. You have around 5 to 7 Extended components (like the LM5163, TPS70933, Fuses), adding **~$15 - $20** in one-time setup fees.
*   **Shipping:** ~$15 to $25 (DHL/FedEx).

### Estimated Budget
*   **Cost of parts per single board:** **~$34.50** (with almost half of this being the $15 Nucleo board). 
*   **Cost for a prototype run of 5 fully assembled boards:** You'll pay around **$175 - $200 total** ($35 - $40 per board). This factors in the JLC assembly fees, the Nucleo boards bought separately, the MOSFETs (if you solder those or buy equivalents), and shipping.