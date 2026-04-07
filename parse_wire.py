import sys
import re

with open("hardware/MCU.kicad_sch", "r") as f:
    text = f.read()

# Very naive check: in KiCad, labels are at some (x y). Wires start/end at (x y).
# We can find the labels and their coordinates.
labels = re.findall(r'\(label "([^"]+)"\n\s*\(at ([\d.-]+) ([\d.-]+) \d+\)', text)

# Find nucleo pins and their coords
pins = re.findall(r'\(pin \w+ line\n\s*\(at ([\d.-]+) ([\d.-]+) \d+\)\n\s*\(length [\d.-]+\)\n\s*\(name "([^"]+)"', text)

print("Labels at coords:")
for name, x, y in labels:
    print(f"  {name}: {x}, {y}")

print("\nPins at coords:")
for x, y, name in pins:
    print(f"  {name}: {x}, {y}")
