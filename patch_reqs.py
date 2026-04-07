import re

with open('Documents/Requirements to bms.md', 'r') as f:
    content = f.read()

power_reqs = """
* POWER CONSUMPTION & HIBERNATION:
	* Active Mode: Capable of supplying stable power for MCU, AFE, and CAN (~50mA).
	* Sleep/Hibernation Target: < 30µA total current draw to prevent battery drain during months of storage.
	* DC-DC Converter: Must feature "Pulse Skipping" / Eco-mode with ultra-low quiescent current (Iq < 15µA) (e.g., LM5163).
	* MCU (STM32L431/L432): Must utilize STOP 2 mode (< 2µA).
	* CAN Transceiver: Must feature Standby pin (STB) to drop consumption (< 5µA) while keeping Wake-on-CAN receiver active.
	* AFE (BQ769x2): Must utilize DEEPSLEEP mode (< 10µA).
"""

# Insert right before SOFTWARE:
content = content.replace("SOFTWARE:", power_reqs + "\nSOFTWARE:")

with open('Documents/Requirements to bms.md', 'w') as f:
    f.write(content)

