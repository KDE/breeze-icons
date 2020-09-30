#!/usr/bin/env python3
"""
SPDX-License-Identifier: LGPL-2.1-only OR LGPL-3.0-only OR LicenseRef-KDE-Accepted-LGPL
SPDX-FileCopyrightText: 2020 Noah Davis <noahadvs@gmail.com>
SPDX-FileCopyrightText: 2020 Niccolò Venerandi <niccolo@venerandi.com>
"""
import os
import unittest
from lxml import etree
"""
This script generates 24px icons based on 22px icons
"""

print("********* Start testing of Test24x24Icons *********")

# BEGIN globals
# These are needed to prevent nonsense namespaces like ns0 from being
# added to otherwise perfectly fine svg elements and attributes
NAMESPACES = {
    "svg": "http://www.w3.org/2000/svg",
    "xlink": "http://www.w3.org/1999/xlink",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape",
    "dc": "http://purl.org/dc/elements/1.1/",
    "cc": "http://creativecommons.org/ns#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
}
for prefix, uri in NAMESPACES.items():
    etree.register_namespace(prefix, uri)

RES_DIR: str = "./res/"
GEN_DIR: str = "./generated/"

# END globals


def get_renderable_elements(root: etree.Element):
    """
    Get renderable elements that are children of the root of the SVG.

    See the Renderable Elements section of the SVG documentaion on MDN web docs:
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element#SVG_elements_by_category
    """
    return root.xpath(
        "./svg:a | ./svg:circle | ./svg:ellipse | ./svg:foreignObject | ./svg:g "
        + "| ./svg:image | ./svg:line | ./svg:mesh | ./svg:path | ./svg:polygon "
        + "| ./svg:polyline | ./svg:rect | ./svg:switch | ./svg:svg | ./svg:symbol "
        + "| ./svg:text | ./svg:textPath | ./svg:tspan | ./svg:unknown | ./svg:use",
        namespaces=NAMESPACES
    )


class Test24x24Icons(unittest.TestCase):

    def test_reverse24x24conversion(self):
        self.maxDiff = None
        for dirpath, dirnames, filenames in os.walk(GEN_DIR):
            for f in filenames:

                # Generated filepath
                gen_filepath = os.path.join(dirpath, f)

                # Filter out files
                if not (f.endswith('.svg') and '/24' in gen_filepath) or os.path.islink(gen_filepath):
                    continue

                etree.set_default_parser(etree.XMLParser(remove_blank_text=True))

                # Generated root
                gen_root = etree.parse(gen_filepath).getroot()

                # Res filepath and root
                res_filepath = gen_filepath.replace(GEN_DIR, RES_DIR, 1).replace('/24', '/22')
                res_root = etree.parse(res_filepath).getroot()

                # Resize to 22x22
                gen_root.set('viewBox', "0 0 22 22")
                gen_root.set('width', "22")
                gen_root.set('height', "22")

                # Remove group that moves content down 1px, right 1px
                group = gen_root.find('./{http://www.w3.org/2000/svg}g', NAMESPACES)
                gen_root.extend(get_renderable_elements(group))
                gen_root.remove(group)

                # Compare elements and attributes
                for gen_elem, res_elem in zip(res_root.iterfind('./svg:*', NAMESPACES),
                                              gen_root.iterfind('./svg:*', NAMESPACES)):
                    self.assertEqual(res_elem.tag, gen_elem.tag, gen_filepath)
                    for attribute in res_elem.items():
                        self.assertIn(attribute, gen_elem.items(), gen_filepath)
                pass


if __name__ == "__main__":
    unittest.main()
