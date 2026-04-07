import re
with open("hardware/frontend.kicad_sch", "r") as f:
    text = f.read()

# Let's find labels connected to the BQ chip. We can't do this easily without a full kicad parser.
# But we can grep for label names in frontend to see what labels are present.
labels = re.findall(r'\(label "([^"]+)"', text)
print("Labels in frontend.kicad_sch:", set(labels))
