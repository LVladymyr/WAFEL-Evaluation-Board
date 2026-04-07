import re
with open("hardware/MCU.kicad_sch", "r") as f:
    text = f.read()

labels = re.findall(r'\(label "([^"]+)"', text)
print("Labels in MCU.kicad_sch:", set(labels))
