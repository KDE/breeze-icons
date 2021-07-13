#!/usr/bin/env python3
"""
SPDX-License-Identifier: LGPL-2.1-only OR LGPL-3.0-only OR LicenseRef-KDE-Accepted-LGPL
SPDX-FileCopyrightText: 2020 Noah Davis <noahadvs@gmail.com>
SPDX-FileCopyrightText: 2020 Niccolò Venerandi <niccolo@venerandi.com>
"""
import os
import re
import sys
from pathlib import Path
from lxml import etree
"""
This script generates 24px icons based on 22px icons
"""

# The BEGIN/END stuff is a Kate/KDevelop feature. Please don't remove it unless you have a good reason.

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

OUTPUT_DIR: str = sys.argv[1]
INPUT_DIR: str = "./"

# END globals


# BEGIN defs

def strip_split(s: str):
    """
    Strip whitespace from the start and end, then split into a list of strings.

    re.split() RegEx: match comma with [0,inf) whitespace characters after it OR [1,inf) whitespace characters.
    """
    # Ignore warnings about invalid escape sequences, this works fine.
    return re.split(",\s*|\s+", s.strip())


def get_renderable_elements(root: etree.Element):
    """
    Get renderable elements that are children of the root of the SVG.

    See the Renderable Elements section of the SVG documentation on MDN web docs:
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element#SVG_elements_by_category
    """
    return root.xpath(
        "./svg:a | ./svg:circle | ./svg:ellipse | ./svg:foreignObject | ./svg:g "
        + "| ./svg:image | ./svg:line | ./svg:mesh | ./svg:path | ./svg:polygon "
        + "| ./svg:polyline | ./svg:rect | ./svg:switch | ./svg:svg | ./svg:symbol "
        + "| ./svg:text | ./svg:textPath | ./svg:tspan | ./svg:unknown | ./svg:use",
        namespaces=NAMESPACES
    )


def main():
    for dirpath, dirnames, filenames in os.walk(INPUT_DIR):
        folder24_destination = os.path.join(dirpath, "24").replace(INPUT_DIR, OUTPUT_DIR, 1)
        for d in dirnames:
            if d != '22':
                continue

            # Make 24/
            Path(folder24_destination).mkdir(parents=True, exist_ok=True)
            # print(folder24_destination)

            # Make 24@2x/ and 24@3x/
            for scale in (2, 3):
                folder24_scaled_destination = folder24_destination.replace('/24', f'/24@{scale}x')
                if os.path.islink(folder24_scaled_destination):
                    os.remove(folder24_scaled_destination)
                os.symlink("24", folder24_scaled_destination, target_is_directory=True)
                # print(folder24_scaled_destination + " -> " + os.readlink(folder24_scaled_destination))

        for f in filenames:
            filepath = os.path.join(dirpath, f)

            # Filter out files
            if not (f.endswith('.svg') and '/22' in filepath):
                continue

            file_destination = filepath.replace(INPUT_DIR, OUTPUT_DIR, 1).replace('/22', '/24')
            # print(file_destination)

            # Regenerate symlinks or edit SVGs
            if os.path.islink(filepath):
                symlink_source = os.readlink(filepath).replace('/22', '/24')
                if os.path.exists(file_destination):
                    os.remove(file_destination)
                os.symlink(symlink_source, file_destination)
                # print(file_destination + " -> " + os.readlink(file_destination))
            else:
                etree.set_default_parser(etree.XMLParser(remove_blank_text=True))
                tree = etree.parse(filepath)
                root = tree.getroot()

                viewBox_is_none = root.get('viewBox') is None
                width_is_none = root.get('width') is None
                height_is_none = root.get('height') is None

                """
                NOTE:
                - Using strip and split because the amount of whitespace and usage of commas can vary.
                - Checking against real values because string values can have leading zeros.
                - Replacing "px" with nothing so that values can be converted to real numbers and because px is the default unit type
                    - If another unit type is used in the <svg> element, this script will fail, but icons shouldn't use other unit types anyway
                """

                # This is used to prevent SVGs with non-square or incorrect but valid viewBoxes from being converted to 24x24.
                # If viewBox is None, but the SVG still has width and height, the SVG is still fine.
                viewBox_matched_or_none = viewBox_is_none
                if not viewBox_is_none:
                    viewBox_matched_or_none = (
                        list(map(float, strip_split(root.get('viewBox').strip('px'))))
                        == [0.0, 0.0, 22.0, 22.0]
                    )

                # This is used to prevent SVGs that aren't square or are missing only height or only width from being converted to 24x24.
                # If width and height are None, but the SVG still has a viewBox, the SVG is still fine.
                width_height_matched_or_none = width_is_none and height_is_none
                if not (width_is_none or height_is_none):
                    width_height_matched_or_none = (
                        float(root.get('width').strip('px').strip()) == 22.0 and
                        float(root.get('height').strip('px').strip()) == 22.0
                    )

                if (width_height_matched_or_none and viewBox_matched_or_none
                        and not (viewBox_is_none and (width_is_none or height_is_none))):
                    # Resize to 24x24
                    root.set('viewBox', "0 0 24 24")
                    root.set('width', "24")
                    root.set('height', "24")
                    # Put content in a group that moves content down 1px, right 1px
                    group = etree.Element('g', attrib={'transform': "translate(1,1)"})
                    group.extend(get_renderable_elements(root))
                    root.append(group)

                    # print(file_destination)
                    tree.write(file_destination, method="xml", pretty_print=True, exclusive=True)
                else:
                    skipped_message = " SKIPPED: "
                    if not viewBox_matched_or_none:
                        skipped_message += "not square or incorrect viewBox\nviewBox=\"" + root.get('viewBox') + "\""
                    elif not width_height_matched_or_none:
                        skipped_message += "not square or incorrect width and height\nwidth=\"" + root.get('width') + "height=\"" + root.get('height') + "\""
                    elif viewBox_is_none and (width_is_none or height_is_none):
                        skipped_message += "viewBox and width/height are missing"
                    else:
                        skipped_message += "You shouldn't be seeing this. Please fix " + os.path.basename(sys.argv[0])

                    print(filepath.lstrip(INPUT_DIR) + skipped_message)

# END defs


# I've structured the program like this in case I want to do multiprocessing later
if __name__ == '__main__':
    sys.exit(main())
