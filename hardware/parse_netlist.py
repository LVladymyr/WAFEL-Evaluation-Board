import xml.etree.ElementTree as ET

tree = ET.parse('netlist.xml')
root = tree.getroot()

# First, find the net with name "+3.3V"
net_3v3 = None
for net in root.findall('.//nets/net'):
    if net.get('name') == '+3.3V':
        net_3v3 = net
        break

if not net_3v3:
    print("Could not find +3.3V net")
    exit(1)

# Get all connected pins
components_on_3v3 = []
for node in net_3v3.findall('node'):
    ref = node.get('ref')
    pin = node.get('pin')
    pinfunction = node.get('pinfunction')
    components_on_3v3.append((ref, pin, pinfunction))

# Now get the details of these components
components_dict = {}
for comp in root.findall('.//components/comp'):
    ref = comp.get('ref')
    value = comp.find('value').text if comp.find('value') is not None else ''
    libsource = comp.find('libsource')
    lib = libsource.get('lib') if libsource is not None else ''
    part = libsource.get('part') if libsource is not None else ''
    description = libsource.get('description') if libsource is not None else ''
    components_dict[ref] = {
        'value': value,
        'lib': lib,
        'part': part,
        'description': description
    }

print(f"Components connected to +3.3V ({len(components_on_3v3)} pins total):\n")
seen_refs = set()
for ref, pin, pinfunction in components_on_3v3:
    if ref not in seen_refs:
        info = components_dict.get(ref, {})
        print(f"{ref} ({info.get('value', 'N/A')} - {info.get('part', 'N/A')}): Pin {pin} ({pinfunction})")
        seen_refs.add(ref)
    else:
        # Just print the additional pin
        info = components_dict.get(ref, {})
        print(f"{ref} ({info.get('value', 'N/A')} - {info.get('part', 'N/A')}): Pin {pin} ({pinfunction})")

