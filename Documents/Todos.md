Also wrote a task list:
1. Configure AFE Thermistors (Route unused pins to FETs, Pre-charge resistor, and Battery cells) 
2. Implement External Cell Balancing (Add external MOSFETs and bleed resistors for >100mA balancing)
3. Route Current Sense (Connect SRP/SRN pins to main Shunt Resistor with RC filter) 
4. Route MOSFET Control Lines (Connect CHG, DSG, PCHG, PDSG to the hs-mosfet board)
5. Replace CAN Transceiver (U802: TJA1051T/3) with a Wake-on-CAN capable IC (e.g., TJA1042T/3 or TCAN1042G)
6. Add isolated optocoupler/SSR circuit and 2-pin connector for the Go-FOC ESC wake/sleep control line
7. Removed 3.3V LDO (U101: TPS70933) as requested
8. Add dedicated dashboard connectors (I2C/SPI, 3.3V/5V) for the OLED display and NFC reader
