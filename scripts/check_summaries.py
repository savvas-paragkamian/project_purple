import xml.etree.ElementTree as ET
import sys

if len(sys.argv) != 2:
    print("Usage: python3 parse_xml.py <file.xml>")
    sys.exit(1)

xml_file = sys.argv[1]

tree = ET.parse(xml_file)
root = tree.getroot()

def print_all(node, indent=0):
    space = "  " * indent
    text = node.text.strip() if node.text else ""
    if text:
        print(f"{space}{node.tag}: {text}")
    else:
        print(f"{space}{node.tag}:")
    for child in node:
        print_all(child, indent + 1)

print_all(root)


# to run the script 
python3 parse_xml.py nameofxml.xml


