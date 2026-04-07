# WAFEL BMS: Requirements & Specifications

## 1. Electrical Characteristics
*   **Cell Configuration:** 6S - 16S Li-ion / LiFePO4 (Voltage range: 21V - 67V).
*   **Operating Current:** 30A Continuous.
*   **Peak Current:** 60A Maximum (Peak discharge).
*   **Charging:** 5A Regular Charge / Up to 15A Regenerative Braking (Recuperation).
    *   *Note: Excess energy above 15A must be handled/shunted.*
*   **MOSFET Specifications:** Vgs/Vds redundancy target: $\ge$ 167V (Pack Max Voltage x 2.5).

## 2. Hardware Architecture
*   **AFE:** Texas Instruments **BQ769x2** series.
*   **MCU:** STMicroelectronics **STM32L432KC** (or L431 variant).
*   **ESC Compatibility:** Optimized for **Go-Foc S100** (VESC-compatible).
*   **Motor Support:** Compatible with 300W - 500W electric engines (including spikes).
*   **Physical Dimensions:** 245mm x 64mm x 16mm.
    *   *Max Height Constraint: 55mm (including batteries).*
    *   *Cell Stack Height (x2): 39mm.*

## 3. Power Management & Hibernation
*   **Sleep/Hibernation Target:** **< 30µA** total standby draw (to support multi-month storage).
*   **Active Mode Supply:**
    *   **Internal BMS Consumption:** ~50mA (MCU, AFE, CAN).
    *   **External Logic Supply (Dashboard):** ~200-300mA provision for NFC reader, OLED Display, etc.
*   **Key Efficiency Mandates:**
    *   **DC-DC Converter:** Must use "Pulse Skipping" / Eco-mode with ultra-low quiescent current (**Iq < 15µA**) (e.g., LM5163).
    *   **MCU:** Must implement **STOP 2 Mode** (< 2µA).
    *   **CAN Transceiver:** Must include a **Standby (STB)** pin and support **Wake-on-CAN** (< 5µA in sleep).
    *   **AFE:** Must utilize hardware **DEEPSLEEP** mode (< 10µA).

## 4. Protection Features
*   **Polarity:** Reverse battery connection protection (+/-).
*   **Electrical Faults:** Reverse electricity and impulse protection.
*   **Inrush Current:** Dedicated **Pre-charge and Pre-discharge** circuitry.
*   **Communication:** CAN bus ESD and transient protection.
*   **Fusing:** Integrated high-current chemical fuse (Self-Control Protector) for catastrophic failures.
*   **Regen current:** 15A for continuous  burst about 5 to 10 seconds from top speed for 300W engine (500W in spike)

## 5. Software & Firmware
*   **Platform:** **Rust-based** firmware implementation.
*   **Protocol:** SPI for AFE communication (enhanced noise immunity).
*   **Features:** Real-time cell monitoring, NFC-triggered Wake-on-CAN boot sequence.

# Attaches
## A. Estimating regen current
Estimating regen current is a mix of physics and ESC configuration. Here is the best way to estimate it for your 300W–500W scooter:
The Physics Calculation:
When you brake, the motor acts as a generator. If your scooter has a 500W motor, under maximum aggressive braking, it can generate roughly 500W of stopping power.
*   Let's assume your battery is at 40V.
*   Current = Power / Voltage
*   $500W / 40V = 12.5A$
*   Factoring in motor/ESC generation efficiency (approx. 80%), the actual current pushed backward into the battery is about 10A.
The Practical (VESC) Reality:
Because you are using a Go-FOC S100 (which runs VESC firmware), you actually get to choose the maximum regen current in software. 
In the VESC Tool, there is a setting called Battery Current Max Regen. 
*   If you set it to -15A, the VESC will simply limit the braking force so it never pushes more than 15A back into the battery. 
*   For a typical e-scooter, setting regen to anything higher than 15A will cause the electronic brake to be so violently strong that it might lock the front wheel or throw the rider over the handlebars! 
Conclusion: Your estimate of 15A max regen in your Requirements document is incredibly accurate for a 500W scooter. Your CHG MOSFETs and battery cells must be rated to handle a 15A continuous burst for about 5 to 10 seconds (the time it takes to brake from top speed to zero).