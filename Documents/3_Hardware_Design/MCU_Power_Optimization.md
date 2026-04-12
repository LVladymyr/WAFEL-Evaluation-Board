# MCU Power Optimization for NUCLEO-L432KC

To meet the strict `< 30µA` hibernation requirement for the BMS, the stock STM32 NUCLEO-L432KC development board requires specific hardware and software modifications. Out of the box, the Nucleo board consumes several milliamps of standby current due to its onboard LDO, ST-LINK debugger, and power LED. 

By performing the following modifications, the Nucleo board can be used as an ultra-low power breakout board powered directly by the BQ76942 AFE's 3.3V `REG1` LDO.

## 1. Hardware Modifications

### A. Remove the Power LED
The power LED on the Nucleo-32 board is hardwired to the 5V/3.3V rail and consumes ~3 mA continuously. 
*   **Action:** Physically desolder, crush, or cut the trace to the Power LED (`LD2` or `LD3`, depending on the board revision).

### B. Isolate the Onboard 3.3V LDO
The onboard LDO (`U3`, LD39050) consumes quiescent current and can leak power backward if 3.3V is supplied externally. According to the **ST UM1956 User Manual**, the board is designed with solder bridges/jumpers specifically for this purpose.
*   **Action (Newer Boards - Rev C+):** Remove the plastic jumper from **`JP1` (IDD)**.
*   **Action (Older Boards):** De-solder or cut the trace on Solder Bridge **`SB14`**.
*   *Result:* This physically disconnects the onboard LDO's output from the main STM32L432KC target MCU.

### C. Powering the Board
After isolating the LDO, the board must be powered externally:
*   Route the 3.3V output from the BQ76942 (`REG1`) directly to the **`+3V3`** pin on the Nucleo header.
*   **Do not** connect any power to the `+5V` or `VIN` pins of the Nucleo.

## 2. Software Modifications (The "Hidden" Drain)

Even with the LDO physically isolated via `JP1`/`SB14`, you may observe an unexplained ~80 µA parasitic drain during deep sleep (STOP 2 mode). 

### The Cause: SWD Pin Leakage
The target STM32L432KC shares the PCB with the ST-LINK debugging chip. The debugging pins (`PA13 / SWDIO` and `PA14 / SWCLK`) are physically wired between the two chips. 
When the BMS is running on battery power (and the USB is disconnected), the ST-LINK chip is unpowered. However, the target STM32 MCU has internal pull-up resistors enabled by default on the SWD pins. These pull-ups leak current directly into the unpowered ST-LINK's internal ESD protection diodes.

### The Fix: Disable Pull-ups Before Sleep
To eliminate this ~80 µA leakage without cutting the physical SWD traces (which would ruin your ability to debug), you must implement a software workaround:

Before placing the MCU into STOP 2 mode, reconfigure the SWD pins to Analog mode. This disables the internal pull-up/pull-down resistors.

```c
// Example C/HAL snippet for entering sleep
GPIO_InitTypeDef GPIO_InitStruct = {0};

// 1. Reconfigure PA13 (SWDIO) and PA14 (SWCLK) to Analog Mode
GPIO_InitStruct.Pin = GPIO_PIN_13 | GPIO_PIN_14;
GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
GPIO_InitStruct.Pull = GPIO_NOPULL;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

// 2. Enter STOP 2 Mode
HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);

// 3. Upon waking up, the SWD pins MUST be reconfigured to their 
//    Alternate Function (AF0) if you wish to attach a debugger again.
```

## 3. Debugging / Reprogramming Workflow
Yes, you can still program and debug the Nucleo board via USB after these modifications!

Because you opened `JP1`/`SB14`, plugging in the USB cable will power up the ST-LINK chip (via the onboard LDO), but **it will not power the target STM32 MCU**.
*   **To program the board:** You must provide external 3.3V power to the `+3V3` pin (e.g., by turning on the BMS battery) *while* the USB cable is plugged in. 
*   This perfectly powers the ST-LINK via USB and the target MCU via the BMS, allowing live, in-circuit debugging under real battery conditions.
