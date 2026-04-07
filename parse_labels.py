import re
with open("hardware/MCU.kicad_sch", "r") as f:
    mcu = f.read()

labels = re.findall(r'\(property "Text" "([^"]+)"', mcu)
print("Labels in MCU.kicad_sch:", set(labels))

with open("hardware/frontend.kicad_sch", "r") as f:
    frontend = f.read()

labels_fe = re.findall(r'\(property "Text" "([^"]+)"', frontend)
print("Labels in frontend.kicad_sch:", set(labels_fe))
