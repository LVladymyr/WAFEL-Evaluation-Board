# WAFEL EVAL BOARD

**Version:** 0.0.1

Evaluation board for the [Texas Instruments BQ76952](https://www.ti.com/product/BQ76952) multi-chemistry battery management IC. Designed to prototype and validate BMS firmware, cell monitoring, and protection circuits.

## Features

- BQ76952 multi-chemistry BMS IC (up to 16S, supports Li-ion, LiFePO4, NiMH)
- LM5164 synchronous buck regulator for on-board power supply
- TPS79333-EP ultra-low-noise LDO
- Charge and discharge MOSFET control path
- Automotive-grade blade fuse holder
- JST GH 17-pin battery connector
- Test points on key signals for bench debugging
- CI/CD pipeline: Gerbers, BOM, PDF schematic, 3D STEP, interactive BOM (iBOM)

## Hardware Overview

| Component | Part | Role |
|-----------|------|------|
| BMS IC | BQ76952 | Cell voltage/temperature monitoring, balancing, protection |
| Buck regulator | LM5164 | Steps down pack voltage to board supply rail |
| LDO | TPS79333-EP | Clean analog/digital supply from buck output |
| Charge FETs | — | Controlled by BQ76952 CHG/DSG pins |
| Connector | JST GH 17-pin | Battery pack interface |
| Fuse | Automotive blade | Pack-level overcurrent protection |

## Repository Structure

```
WAFEL_EVAL_BOARD/
├── *.kicad_pro        # KiCad project file
├── *.kicad_sch        # Schematic
├── *.kicad_pcb        # PCB layout
├── *.kicad_dru        # Design rules
├── fp-lib-table       # Footprint library table
├── sym-lib-table      # Symbol library table
├── .github/
│   └── workflows/     # CI/CD pipeline (KiBot)
└── README.md
```

## CI/CD & Manufacturing Outputs

Commits to `main` trigger a [KiBot](https://github.com/INTI-CMNB/KiBot) workflow via GitHub Actions that automatically generates:

- **Gerbers** — production-ready fabrication files
- **BOM** — bill of materials (CSV)
- **PDF** — schematic and PCB drawings
- **3D STEP** — mechanical model for enclosure design
- **iBOM** — interactive HTML BOM for assembly

Artifacts are attached to each workflow run.

## Getting Started

1. Install [KiCad 9.0](https://www.kicad.org/download/)
2. Clone this repository
3. Open the `.kicad_pro` file in KiCad

## License

Hardware design files are licensed under the **CERN Open Hardware Licence Version 2 – Strongly Reciprocal (CERN-OHL-S v2)**.
See [https://ohwr.org/cern_ohl_s_v2.txt](https://ohwr.org/cern_ohl_s_v2.txt) for the full license text.
