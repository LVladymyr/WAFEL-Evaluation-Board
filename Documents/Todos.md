Also wrote a task list:
1. Configure AFE Thermistors (Route unused pins to FETs, Pre-charge resistor, and Battery cells) 
2. Implement External Cell Balancing (Add external MOSFETs and bleed resistors for >100mA balancing)
3. Route Current Sense (Connect SRP/SRN pins to main Shunt Resistor with RC filter) 
4. Route MOSFET Control Lines (Connect CHG, DSG, PCHG, PDSG to the hs-mosfet board)
5. Replace CAN Transceiver (U802: TJA1051T/3) with a Wake-on-CAN capable IC (e.g., TJA1042T/3 or TCAN1042G)
6. Add isolated optocoupler/SSR circuit and 2-pin connector for the Go-FOC ESC wake/sleep control line
7. Removed 3.3V LDO (U101: TPS70933) as requested
8. Add dedicated dashboard connectors (I2C/SPI, 3.3V/5V) for the OLED display and NFC reader

Termoresitors:
Where should we place these 6 Thermistors? (The Critical Zones)
For a 60A peak e-scooter, thermal management is your biggest enemy. Here is exactly where you should place the 6 available thermistors, in order of absolute importance:
1.  The Discharge MOSFETs (DSG FETs) Critical
    *   Why: At 60A, these FETs will generate massive heat. If they exceed ~125°C, they will fail closed (permanently ON), causing a catastrophic safety hazard.
    *   Placement: Physically touching the copper pour right next to the DSG FETs on your hs-mosfet board.
2.  The Pre-Charge Resistor Critical
    *   Why: When you tap your NFC, the pre-charge resistor limits the inrush current to the ESC. If the ESC has a short circuit, this resistor will take the full pack voltage and will catch fire in seconds. 
    *   Placement: Glued or copper-routed directly adjacent to the pre-charge resistor body.
3.  The Battery Core (Center) Critical
    *   Why: The cells in the very middle of the battery pack have the worst airflow and get the hottest during heavy riding.
    *   Placement: A wired NTC thermistor taped between the middle cells.
4.  The External Balancing Resistors High
    *   Why: Because you are implementing 100mA+ external balancing, those bleed resistors will get very hot during the end of a charge cycle. You want the AFE to pause balancing if the PCB is melting.
    *   Placement: In the center of the balancing resistor matrix on the main BMS board.
5.  The Charge MOSFETs (CHG FETs) Medium
    *   Why: Normally charging is only 5A (low heat), but you mentioned 15A regenerative braking. 15A pushed backward through the CHG FETs will generate significant heat.
    *   Placement: On the copper pour next to the CHG FETs.
6.  The Battery Edge (Ambient) Medium
    *   Why: Placed on the outside edge of the cell pack. By comparing the "Core" temperature to the "Edge" temperature, your STM32 can calculate the thermal gradient and detect if a single cell is undergoing thermal runaway before it affects the whole pack.