#!/usr/bin/env python3
"""
SPDX-License-Identifier: LicenseRef-KDE-Accepted-LGPL
SPDX-FileCopyrightText: 2020 Noah Davis <noahadvs@gmail.com>
SPDX-FileCopyrightText: 2020 Niccolò Venerandi <niccolo@venerandi.com>
"""
import sys
from lxml import etree
"""
This is a template for making scripts that modify SVGs by parsing XML.
"""

# These are needed to prevent nonsense namespaces like ns0 from being
# added to otherwise perfectly fine svg elements and attributes
etree.register_namespace("w3c", "http://www.w3.org/2000/svg")
etree.register_namespace("xlink", "http://www.w3.org/1999/xlink")
etree.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
etree.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
etree.register_namespace("cc", "http://creativecommons.org/ns#")
etree.register_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
etree.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

# Get filenames as arguments. Combine with your favorite CLI tools.
# My favorites are rg (aka ripgrep) and fd (aka fd-find).
# Remember to filter out files that are not SVGs!
# Example: ./this-script.py $(rg -t svg -l 'height="0"')
for f in sys.argv[1:]:
    tree = etree.parse(f)
    root = tree.getroot()
    wasEdited = False

    # BEGIN section
    # Reimplement this section as needed
    # {http://www.w3.org/2000/svg} is needed to find SVG elements
    # Example: find all rect elements
    for elem in root.iterfind(".//{http://www.w3.org/2000/svg}rect"):
        # Example: find rect elements where height="0"
        if (elem.get("height") == "0"):
            # Example: remove rect elements that have height="0"
            elem.getparent().remove(elem)
            wasEdited = True  # Remember to keep this
    # END section

    print(f + ": " + ("edited" if wasEdited else "ignored"))
    if wasEdited:
        tree.write(f, encoding="utf-8", xml_declaration=False, method="xml")
