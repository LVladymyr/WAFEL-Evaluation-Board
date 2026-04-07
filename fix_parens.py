import re

with open('hardware/wafel-eval-board.kicad_sym', 'r') as f:
    content = f.read()

# Fix the bad parenthesis before the CAN symbol
content = content.replace("\t)\n\t)\n  (symbol \"CAN_Transceiver_8Pin\"", "\t)\n  (symbol \"CAN_Transceiver_8Pin\"")

with open('hardware/wafel-eval-board.kicad_sym', 'w') as f:
    f.write(content)

