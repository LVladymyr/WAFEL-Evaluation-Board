# WAFEL BMS: Requirements & Specifications

## 1. Electrical Characteristics
*   **Cell Configuration:** 6S - 10S Li-ion / LiFePO4 (Voltage range: 21V - 42V).
*   **Operating Current:** 30A Continuous.
*   **Peak Current:** 60A Maximum (Peak discharge).
*   **Charging:** 5A Regular Charge / Up to 15A Regenerative Braking (Recuperation).
    *   *Note: Excess energy above 15A must be handled/shunted.*
*   **MOSFET Specifications:** Vgs/Vds redundancy target: $\ge$ 105V (Pack Max Voltage x 2.5).

## 2. Hardware Architecture
*   **AFE:** Texas Instruments **BQ7694204** (10S version).
    *   Provides SPI interface with CRC at 3.3V for reliable communication.
    *   Utilizes **REG1** for 3.3V output (perfect for MCU and logic).
    *   Utilizes **REG2** for 5V output (perfect for CAN transceivers).
*   **MCU:** STMicroelectronics **STM32L432KC** (or L431 variant).
*   **ESC Compatibility:** Optimized for **Go-Foc S100** (VESC-compatible).
    *   *Improvement (Ref: Go-FOC Manual):* The Go-FOC S100 features a dedicated "SWITCH" pin (on the COMM port) for ultra-low power sleep mode. The BMS hardware MUST include a logic-level control line (e.g., an isolated optocoupler or small solid-state relay) to interface directly with this switch pin. This allows the BMS to gracefully shut down or wake up the ESC (e.g., during NFC lock, inactivity, or soft-faults) without needing to abruptly cut the heavy main discharge MOSFETs under load.
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
    *   *Improvement (Ref: VESC Manual & Go-FOC):* A hardware brake shunt is often too bulky and generates too much heat for a standard 300W-500W scooter chassis. Instead, the preferred and standard industry solution is **Dynamic CAN Throttling combined with VESC Ramping**. As the battery approaches 100% SoC, the BMS must use the CAN bus to *smoothly ramp down* the allowed charge current limit toward 0A. The VESC's internal algorithms (and parameters like Negative Ramping Time) will gracefully fade the electronic braking force without sudden jerks. At 100% SoC, the rider will naturally have reduced electronic brakes and must rely on the scooter's mechanical brakes. **Critical Safety Requirement:** The BMS must NEVER abruptly open the CHG MOSFETs during regen, as this instantly disconnects the battery, causing a massive voltage spike, a VESC OVER_VOLTAGE fault, and a violent, instantaneous loss of all motor resistance.
*   **Voltage Cutoff Coordination:** 
    *   *Improvement (Ref: VESC Manual - Motor Wizard FOC):* The BMS Under-Voltage Protection (UVP) must be set slightly *lower* (e.g., 2.9V - 3.0V/cell) than the VESC's configured hard cutoff (e.g., 3.1V/cell). This ensures the VESC performs a graceful power taper rather than the BMS abruptly cutting system power and throwing the rider.
*   **Overcurrent Protection (OCP) Tuning:**
    *   *Improvement:* The AFE (BQ76942) short-circuit and over-current delays must be carefully tuned to tolerate harmless micro-second inrush/transient spikes from the Go-FOC S100 (which can theoretically pull up to 200A) without tripping the 60A peak limit prematurely.

## 5. Software & Firmware
*   **Platform:** **Rust-based** firmware implementation.
*   **Protocol:** SPI for AFE communication (enhanced noise immunity).
*   **Features:** Real-time cell monitoring, NFC-triggered Wake-on-CAN boot sequence.
*   **VESC CAN Integration:**
    *   *Improvement:* Firmware must explicitly support the **VESC CAN Protocol**. The BMS must broadcast its real-time status (pack voltage, cell voltages, temperature, dynamic discharge/charge limits) to the Go-FOC S100. By smoothly broadcasting a decreasing charge limit as the battery hits 100% SoC, the VESC will safely and gradually reduce electronic braking power, keeping the hardware safe while giving the rider a smooth, predictable transition to mechanical brakes.

## 6. Assembly requirement
* Not use complex to sold components!
* Not use small SMD componnts, only some that could be added with cheap hot air soldering gun

## 7. Cost requirement
* **Designed PCB** should cost less then 70 USD of parts without soldering [[budget_estimate]]

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