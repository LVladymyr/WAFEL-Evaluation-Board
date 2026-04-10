# Generic

Will use STM32L432KC MCU as it reasonably cheap, has rust support (that very interesting to me), has hardware can and low power.

The STM32L432KC (and the Nucleo-32 development board specifically) is an absolutely perfect choice for your e-scooter project. 
While we haven't explicitly discussed the MCU selection in this immediate chat, here is why this specific chip is the ideal brain for both your BMS and your Dashboard:
1. The "L" stands for Ultra-Low Power
This is the most important reason! The STM32L4 series is explicitly designed for battery-powered applications. 
*   Earlier we talked about how your Dashboard must stay alive 24/7 to listen for the NFC tag. 
*   The STM32L432KC has incredible Deep Sleep and Stop modes. It can sleep while consuming less than 1.5 µA (micro-amps), while keeping its RAM active and waiting for a pin interrupt (like the CAN RX pin waking up, or the NFC chip triggering a read). This ensures your scooter battery won't die over the winter.
2. Built-in Hardware CAN (bxCAN)
Not all microcontrollers have CAN bus built-in (for example, standard Arduinos or standard ESP32s require external SPI-to-CAN chips like the MCP2515). 
*   The STM32L432KC has a dedicated hardware CAN controller right on the silicon. 
*   This makes your CAN communication with the VESC much more reliable, much faster, and frees up CPU time, requiring only the tiny 8-pin CAN transceiver (like the TJA1051T we just added) to connect to the physical bus.

In short: It gives you ARM Cortex-M4 performance (80MHz), hardware CAN, and NFC connectivity, all while sipping practically zero battery power when the scooter is locked!

In first iteration will use NUCLEO testing board
1. Tiny Form Factor (Nucleo-32)
Since you are building an evaluation board (WAFEL_EVAL_BOARD), using the Nucleo-L432KC module is highly strategic.
*   It has the exact same footprint as an Arduino Nano.
*   It is small enough to actually fit inside a real e-scooter dashboard or battery enclosure during your prototyping phase.
*   It has a built-in ST-LINK debugger on the bottom, meaning you don't need any external programmers to flash code or debug your CAN/NFC logic.
2. Perfect Peripheral Mix
For your Dashboard, you need to talk to an NFC reader (usually via SPI or I2C) and perhaps a small OLED display. For the BMS, you need to talk to the AFE (Analog Front End) via I2C. The STM32L432 has multiple hardware SPI and I2C buses, allowing you to easily handle the interaction with AFE, a display, and the CAN bus all at the exact same time without bottlenecks.


# CAN Bus

## Data & Control Connections (To MCU)

The STM32L432KC has a dedicated hardware CAN controller. Its default pins are PA11 (RX) and PA12 (TX). On the Nucleo-32 board, these are routed to specific headers:
*   U2 Pin 1 (TXD) ➜ Connect to Nucleo CN3_5 (This is pin PA12 / Arduino D2)
*   U2 Pin 4 (RXD) ➜ Connect to Nucleo CN3_13 (This is pin PA11 / Arduino D10)
*   U2 Pin 8 (STB) ➜ Connect to Nucleo CN3_6 (This is pin PB0 / Arduino D3). 
    *   Note: You can actually use any free digital pin for STB, but D3 is right next to the TX pin so it makes the schematic routing clean.
# Analog Front End (AFE)

## Communication Protocol: SPI vs I2C
For an e-scooter BMS, **SPI is the highly recommended protocol over I2C.**
1. **EMI / Noise Immunity (The biggest reason):** E-scooters have high-power ESCs drawing dozens of amps, creating massive electromagnetic interference (EMI). I2C uses "open-drain" pins with pull-up resistors, which are susceptible to magnetic noise. SPI uses "push-pull" pins, actively driving lines to a hard 3.3V or 0V, making it incredibly resistant to electrical noise.
2. **Speed:** SPI can run at 2 MHz+, allowing the MCU to read all cell voltages and temperatures almost instantly. I2C maxes out at 400 kHz.
3. **CRC Safety:** While both support CRC for data integrity, SPI's speed allows its use without bogging down the MCU's cycle time.

*Note: While some reference designs use I2C for general-purpose evaluation, SPI is the industry standard for a real electric vehicle AFE.*

## Pin Assignments (STM32L432KC Nucleo-32)
These hardware SPI pins do not conflict with the CAN bus pins. We will use the MCU's `SPI1` hardware block.

*   **SCK (Clock):** Nucleo `CN4_15` (Pin PB3 / Arduino D13)
*   **MISO (Data from AFE to MCU):** Nucleo `CN4_14` (Pin PB4 / Arduino D12)
*   **MOSI (Data from MCU to AFE):** Nucleo `CN4_13` (Pin PB5 / Arduino D11)
*   **CS (Chip Select):** Nucleo `CN3_11` (Pin PA4 / Arduino A3) - *Any free GPIO works, PA4 is convenient.*

### Crucial Addition: The ALERT Pin
Regardless of the bus used, the AFE requires an **ALERT** or **INT** (Interrupt) pin. This is a physical wire the AFE uses to instantly signal faults like "SHORT CIRCUIT!" or "OVERVOLTAGE!" to the MCU, rather than waiting for the MCU to poll for data.

*   **AFE ALERT:** Nucleo `CN3_12` (Pin PA9 / Arduino D8)
