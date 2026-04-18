import xml.etree.ElementTree as ET

tree = ET.parse('netlist.xml')
root = tree.getroot()

for net in root.findall('.//nets/net'):
    print(net.get('name'))
