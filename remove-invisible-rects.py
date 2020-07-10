#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET


def process(f):
    tree = ET.parse(f)
    root = tree.getroot()
    wasEdited = False
    for rect in root.iterfind("./{http://www.w3.org/2000/svg}rect"):
        print(rect)
        if (rect.get("width") == "0"):
            root.remove(rect)
            wasEdited = True
    if wasEdited:
        tree.write(f, encoding="utf-8", xml_declaration=False, method="xml")


ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
ET.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
ET.register_namespace("cc", "http://creativecommons.org/ns#")
ET.register_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
ET.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
for f in sys.argv[1:]:
    process(f)


"""
with open(d := os.path.join(dir, f), 'r') as file:
    text = file.read().replace('color...', 'newcolor...').replace(..., ...)
with open(d, 'w') as file:
    file.write(text)
"""
