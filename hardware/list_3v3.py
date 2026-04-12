import xml.etree.ElementTree as ET

tree = ET.parse('netlist.xml')
root = tree.getroot()

net_3v3 = None
for net in root.findall('.//nets/net'):
    if net.get('name') == '+3.3V':
        net_3v3 = net
        break

comps = {}
for comp in root.findall('.//components/comp'):
    ref = comp.get('ref')
    val = comp.find('value').text if comp.find('value') is not None else ''
    libsource = comp.find('libsource')
    desc = libsource.get('description') if libsource is not None else ''
    comps[ref] = {'val': val, 'desc': desc}

print("Components connected to +3.3V:")
for node in net_3v3.findall('node'):
    ref = node.get('ref')
    pin = node.get('pin')
    function = node.get('pinfunction')
    print(f"- {ref} ({comps[ref]['val']}): Pin {pin} ({function}) - {comps[ref]['desc']}")
