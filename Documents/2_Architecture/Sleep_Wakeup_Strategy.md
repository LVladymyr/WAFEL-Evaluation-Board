# E-Scooter BMS Power Management: Sleep & Wake-up Strategy

This document outlines the exact hardware and firmware sequence required to put the e-scooter BMS into an ultra-low-power sleep state when parked, and how to instantly wake it up over the CAN bus when the user taps their NFC tag.

## The Hardware Actors
1. **MCU (STM32L432KC):** Acts as the master controller. Capable of ultra-low-power STOP modes while retaining RAM and GPIO interrupt capabilities.
2. **CAN Transceiver (TCAN1042 / TJA1051T):** Interfaces with the physical CAN bus. Has a dedicated Standby (`STB`) pin and outputs wake-up events on the `RXD` pin.
3. **AFE (e.g., TI BQ7694204):** Monitors battery cells. Has its own DEEPSLEEP/SHUTDOWN modes to minimize cell drain.

---

## 1. The Sleep Sequence (Shutdown)
When the scooter is locked, the BMS must reduce its power consumption from ~50-100mA down to <10µA to prevent battery drain over long periods.

**Firmware Steps:**
1. **Put AFE to Sleep:** The STM32 sends a command over SPI to put the AFE into `DEEPSLEEP` mode.
   * *Reference:* BQ7694204 Technical Reference Manual (TRM) - "Power Modes" (DEEPSLEEP disables the ADC but keeps internal regulators alive, drawing ~9µA).
2. **Put CAN Transceiver to Sleep:** The STM32 drives the `STB` pin (PB0) **HIGH**.
   * *Reference:* TCAN1042/TJA1051T Datasheet - "Operating Modes". Driving STB high disables the transmitter, dropping current from ~50mA to ~2µA. The receiver remains active in a low-power listening state.
3. **Configure the Wake-Up Interrupt:** The STM32 configures the `RXD` pin (PA11) as an External Interrupt (EXTI) mapped to trigger on a **Falling Edge** (High-to-Low transition).
   * *Reference:* STM32L432 Reference Manual (RM0394) - "Extended interrupts and events controller (EXTI)".
4. **MCU Enters Deep Sleep:** The STM32 executes the `WFI` (Wait For Interrupt) assembly instruction and enters **STOP 2 Mode**.
   * *Reference:* STM32L432 Reference Manual (RM0394) - "Power control (PWR)". STOP 2 mode turns off the main clocks (PLL, HSI) but retains SRAM and allows EXTI pins to wake the CPU, drawing ~1.5µA.

---

## 2. The Parked State (Idling)
* The entire BMS (MCU + AFE + CAN Transceiver) is consuming roughly **5 to 15µA** from the shared DC-DC converter.
* The CAN bus `CAN_H` and `CAN_L` lines sit at a recessive voltage of ~2.5V.
* The CAN transceiver keeps the `RXD` pin pulled **HIGH (3.3V)**.

---

## 3. The Wake-Up Sequence (The NFC Tap)
When the user taps their NFC tag, the Dashboard powers up and must wake the rest of the scooter.

**Hardware & Firmware Steps:**
1. **Dashboard Sends a WUP:** The Dashboard transmits a CAN message (e.g., ID `0x000` with no data). This creates a dominant voltage differential on the bus (CAN_H > 3.5V, CAN_L < 1.5V).
2. **Transceiver Detects WUP:** The sleeping CAN transceiver detects this Wake-Up Pattern (WUP).
   * *Reference:* TCAN1042 Datasheet - "Remote Wake-Up via CAN". 
3. **Hardware Alarm Triggered:** The CAN transceiver instantly pulls its `RXD` pin **LOW (0V)** to signal the MCU.
4. **MCU Wakes Up:** The High-to-Low transition on `RXD` triggers the STM32's EXTI hardware. The STM32 exits STOP 2 mode, restores its system clocks, and resumes code execution inside the EXTI Interrupt Service Routine (ISR).
5. **Restore CAN TX:** The STM32's first action is to drive the `STB` pin **LOW**. This fully powers up the CAN transmitter so the BMS can reply.
6. **Wake AFE and Power Up:** The STM32 sends a wake command to the AFE and toggles the `ENABLE` pin on the High-Side MOSFET board to supply raw battery power to the ESC.

---

## 4. Crucial Firmware Rule: "The Missed Message"
Because the STM32 is in STOP 2 mode, it takes a few microseconds for the internal oscillators to spin up and for the MCU to pull the `STB` pin low. During this brief boot-up window, the CAN peripheral is not yet ready to process incoming packets.

As a result, **the BMS will physically fail to read the very first CAN message** that woke it up.

**Solution for the Dashboard Firmware:**
1. Send a "Dummy Wake-Up" CAN message (e.g., ID `0x000`).
2. Delay for **10 to 50 milliseconds** to allow the BMS MCU to wake up, reconfigure its clocks, and initialize the bxCAN peripheral.
3. Send the actual "System Enable" or "Status Request" CAN message.

## 5. The Role of DC-DC Converters During Hibernation
**The logic DC-DC converters must NOT be turned off (disabled) during hibernation.** They must remain active 24/7 to provide power to the STM32 and the CAN transceiver's low-power receiver. If the DC-DC is disabled, the BMS cannot detect a wake-up signal from the Dashboard.

Instead of shutting off, the system relies on the DC-DC converter entering **Pulse Skipping Mode (or Eco-Mode)**.

### Pulse Skipping & Ultra-Low Quiescent Current (Iq)
When the MCU, AFE, and CAN transceiver enter their sleep states, the total current draw drops from ~50mA down to roughly ~15µA. A modern, efficient DC-DC converter detects this massive drop in load and stops switching at its normal high frequency (e.g., 1 MHz). 

Instead, it pulses the inductor occasionally to top up the output capacitors and then turns its internal circuitry off to save power. 

**The Golden Rule for Component Selection:**
You must select a DC-DC converter with an **Ultra-Low Quiescent Current (Iq)** specification. 
*   *Bad Choice:* Standard hobbyist converters (like LM2596 or XL7015) have an Iq of ~5mA (5000µA). They will drain a scooter battery in weeks even if the MCU is sleeping.
*   *Good Choice:* The TI **LM5163** (used in the TIDM-788 reference design) has an Iq of **10µA**. 

### Estimated Hibernation Power Budget (BMS Only)
When the scooter is parked and locked, the power consumption is distributed as follows:
*   **STM32L432KC (STOP 2 Mode):** ~1.5 µA
*   **CAN Transceiver (Standby):** ~2.0 µA
*   **AFE (Deep Sleep, e.g., BQ7694204):** ~9.0 µA
*   **DC-DC Converter (e.g., LM5163 Eco-Mode):** ~10.0 µA
*   **Total BMS Standby Drain:** **~22.5 µA**

At 22.5 µA, the BMS alone would take decades to drain a standard 10Ah e-scooter battery. This demonstrates why selecting an ultra-low Iq DC-DC converter is critical for long-term storage without disabling the power supply.

---

## 6. Disabling the Go-FOC ESC (Graceful Shutdown)
When the scooter is parked, locked via NFC, or encounters a non-critical fault, the BMS must shut down the motor controller to save power and secure the vehicle. 

**The Wrong Way (Hardware Cutoff):** Abruptly opening the massive CHG/DSG MOSFETs on the battery line while the ESC is powered on. This can cause voltage spikes and stresses the BMS hardware.

**The Right Way (Go-FOC SWITCH Pin):**
As documented in the *Go-FOC Series ESC - General Operation Manual (Page 3, Port Description)*, the Go-FOC S100 features a dedicated **SWITCH** pin on its 8-pin COMM port. This pin allows the device "to be set into ultra-low power sleep mode."

### Hardware Requirement:
*   The BMS schematic MUST include a dedicated, logic-level control line connected to an STM32 GPIO.
*   Because the BMS and ESC might have slight ground offsets or noise, this control line should ideally use a small **optocoupler** or solid-state relay to interface with the Go-FOC's `SWITCH` pin. 
*   *Wiring:* The optocoupler will short the Go-FOC's `SWITCH` pin to the Go-FOC's `GND` pin (both located on the COMM port) to toggle its power state, exactly as a physical push-button would.

### Firmware Requirement:
*   **Sleep Sequence Addition:** During the Sleep Sequence (Section 1), before the STM32 puts the AFE and CAN transceiver to sleep, it must assert the GPIO connected to the Go-FOC `SWITCH` optocoupler to put the ESC into its ultra-low power sleep mode.
*   **Wake Sequence Addition:** During the Wake-Up Sequence (Section 3), after the STM32 wakes up and restores CAN, it must toggle the Go-FOC `SWITCH` optocoupler to wake the ESC up.
*   **Software Configuration:** The Go-FOC must be configured via the VESC Tool to recognize this pin. As per the manual (Page 8), the "Shutdown Mode" in VESC App Settings must be configured (e.g., `OFF_AFTER_30M` or another appropriate setting that enables the switch functionality) rather than `ALWAYS ON`.

---

## 7. AFE (BQ7694204) Specific Functional Modes
To ensure the BMS perfectly tracks the scooter's real-world states and can recover from edge cases (like extreme low voltage), the firmware must manage the 4 hardware states of the BQ7694204 AFE:

### State 1: NORMAL MODE (Active Riding)
*   **Behavior:** Full ADC monitoring, all protections active, regulators on.
*   **Trigger:** Actively riding the scooter or charging.

### State 2: SLEEP MODE (Stopped / Idling)
*   **Behavior:** Saves power while stopped (e.g., at a traffic light). The ADC slows down (Periodic ADC protections), but the hardware "Current wake detector" stays active.
*   **Trigger:** Entered *automatically* by the AFE when it detects "Low current" (throttle released).
*   **Wake-Up:** The moment the throttle is pressed, the current draw kicks the AFE back to NORMAL MODE automatically without MCU intervention.

### State 3: DEEPSLEEP MODE (Parked / Locked / Hibernation)
*   **Behavior:** ADC is off, protections are off. Only internal regulators and a low-frequency oscillator (LFO) remain on. Consumption drops to ~10µA.
*   **Trigger:** The STM32 sends the `DEEPSLEEP()` SPI command **twice** (to prevent accidental triggering). Also entered on a "Permanent Fail".
*   **Wake-Up:** The STM32 sends `EXIT_DEEPSLEEP()` over SPI or toggles the hardware `RST_SHUT` pin.

### State 4: SHUTDOWN MODE (Absolute Emergency / Deep Discharge)
*   **Behavior:** Total blackout to save the cells from irreversible damage. Regulators turn off. Consumption drops to ~1µA. **The SPI/I2C buses are completely dead.** The STM32 cannot communicate with the AFE.
*   **Trigger:** Triggered automatically by "Very low V_BAT", "high temp", or a specific shutdown command. 
*   **Wake-Up:** Because SPI is dead, the MCU *cannot* wake the AFE via software. It can **only** be woken by hardware: "Charger detection" (plugging it in) or "TS2 pulldown detection".

### Critical Hardware Pin Requirements (To-Do for Schematic)
To guarantee the MCU can control and recover the AFE across all these states, the following physical pins must be wired correctly in the schematic:
1.  **RST_SHUT Pin:** Must connect to an STM32 GPIO. This provides a hardware override to wake the AFE from DEEPSLEEP or hard-reset it if the SPI bus hangs.
2.  **TS2 Pin:** Must connect to an STM32 GPIO via a small N-channel MOSFET (or BJT) to ground. If the AFE enters full SHUTDOWN, pulling this pin to ground is the *only* way the MCU can wake it back up without a charger.
3.  **LD Pin (Load/Charger Detect):** Must be correctly wired to the `PACK+` side so that plugging in a charger automatically wakes the AFE from SHUTDOWN or DEEPSLEEP.
