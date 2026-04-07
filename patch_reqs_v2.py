import re

with open('Documents/Requirements to bms.md', 'r') as f:
    content = f.read()

# Refine the Active Mode point
old_active = r"\* Active Mode: Capable of supplying stable power for MCU, AFE, and CAN \(~50mA\)."
new_active = """* Active Mode:
		* Internal (BMS): ~50mA for MCU, AFE, and CAN.
		* External (Dashboard): Capable of supplying ~200-300mA for Dashboard (NFC reader, Display, MCU, etc.) via the same low-power DC-DC or a dedicated auxiliary line."""

content = re.sub(old_active, new_active, content)

with open('Documents/Requirements to bms.md', 'w') as f:
    f.write(content)

