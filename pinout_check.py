import re
with open('hardware/MCU.kicad_sch', 'r') as f:
    text = f.read()

# find U1 symbol
matches = re.finditer(r'\(symbol "NUCLEO-L432KC_1_0"(.*?)\)', text, re.DOTALL)
for m in matches:
    print(m.group(0))
