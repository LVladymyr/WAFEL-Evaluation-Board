import sys
import re

with open("Documents/MCU.md", "r") as f:
    mcu = f.read()

# I am looking for the TIDA-010208 schematic PDF text, which was extracted before
