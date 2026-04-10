# VESC-Compatible Recuperation Strategy (Regenerative Braking)

## 1. Overview
This document outlines the regenerative braking (recuperation) strategy for the WAFEL BMS, specifically tailored for integration with VESC-compatible ESCs like the **Go-FOC S100** on a 300W-500W electric scooter.

The core challenge in any electric vehicle design is managing regenerative braking energy when the battery is already fully charged (100% State of Charge / SoC).

## 2. The Core Challenge: Braking at 100% SoC
When a rider applies the electronic brake, the motor acts as a generator, pushing current (up to 15A / 500W for our system) back into the battery. 

If the battery is already at 100% SoC, it cannot safely absorb this energy without risking over-voltage, cell swelling, or thermal runaway. The energy must go somewhere, or the braking must be disabled.

### Rejected Solution: Hardware Brake Chopper / Shunt Resistors
*   **Concept:** Burn the excess energy as heat using massive power resistors.
*   **Why we rejected it:** Dissipating 500W of power requires large heat sinks and heavy, expensive resistors. This is completely impractical for the compact, lightweight chassis of a standard e-scooter.

---

## 3. The Adopted Strategy: Dynamic CAN Throttling & Mechanical Reliance

Instead of burning energy as heat, our architecture relies on **Smart Software Limits via CAN bus** combined with **VESC Ramping Algorithms** and the rider's reliance on **Mechanical Brakes**.

### How it Works ("The 3 Phases")

1.  **Phase 1: Battery is Full (100% SoC)**
    *   The BMS monitors the cell voltages. Seeing they are at max (e.g., 4.2V/cell), the BMS broadcasts a CAN message to the Go-FOC: **`Charge Current Limit = 0A`**.
    *   The VESC gracefully disables electronic braking.
    *   *Rider Experience:* The rider feels no motor resistance when pressing the electronic brake and must rely entirely on the scooter's mechanical brakes (disc/drum).

2.  **Phase 2: Battery is Slightly Discharged (~95% SoC)**
    *   The battery has room to absorb some energy. The BMS updates the CAN message: **`Charge Current Limit = 5A`**.
    *   The VESC uses its internal "Negative Ramping Time" to smoothly enable mild regenerative braking without jerking the rider.
    *   *Rider Experience:* The electronic brake provides gentle stopping assistance.

3.  **Phase 3: Battery is Discharged (< 90% SoC)**
    *   The battery can safely absorb the maximum rated braking burst. The BMS broadcasts: **`Charge Current Limit = 15A`**.
    *   *Rider Experience:* Full electronic braking power (500W) is available.

---

## 4. 🚨 CRITICAL SAFETY RULE: Never Abruptly Open CHG MOSFETs 🚨

The entire purpose of the CAN-based dynamic throttling strategy is to **prevent the BMS hardware from having to intervene during normal riding.**

**The Danger of Hardware-Only Protection:**
If the BMS *does not* throttle the VESC via CAN, the VESC will push 15A into a full battery. The BMS AFE (BQ76942) will detect an Over-Voltage (OV) condition and instantly open the Charge (CHG) MOSFETs to protect the cells. 

**This causes a catastrophic sequence of events:**
1.  The energy flowing from the motor suddenly has nowhere to go.
2.  The voltage on the ESC's DC bus spikes massively within milliseconds.
3.  The VESC detects this and throws an `OVER_VOLTAGE` fault.
4.  The VESC instantly disables the motor to save its own hardware.
5.  **The rider experiences a violent, instantaneous loss of all motor braking resistance**, potentially throwing them off balance or causing an accident.

### Architecture Requirement for Firmware (Rust)
The Rust firmware MUST implement a predictive ramping curve. It must monitor maximum cell voltage and dynamically scale down the broadcasted `Max Regen Current` well before the hardware Over-Voltage Protection (OVP) threshold is reached. 

**Hardware OVP (opening the CHG MOSFET) must be treated as a catastrophic failure failsafe, NOT a normal operational braking limit.**