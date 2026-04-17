import sys
import re
from glob import glob

components = []

for sch_file in glob("*.kicad_sch"):
    with open(sch_file, "r") as f:
        content = f.read()
        
    # very basic heuristic: find components
    # Better approach is to use KiCad Python API if available, but it might not be.
    # Alternatively, just grep for Value and Footprint
    pass

