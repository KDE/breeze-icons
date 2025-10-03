#!/usr/bin/env python3
"""
SPDX-License-Identifier: LicenseRef-KDE-Accepted-LGPL
SPDX-FileCopyrightText: 2020 Noah Davis <noahadvs@gmail.com>
SPDX-FileCopyrightText: 2020 Niccolò Venerandi <niccolo@venerandi.com>
SPDX-FileCopyrightText: Louis Moureaux <m_louis30@yahoo.com>
"""
import argparse
import os
import sys
from copy import copy
from lxml import etree
from subprocess import run
from typing import Optional
"""
Generates battery icons.
"""

def save(tree: etree.Element, filename: str) -> None:
    """
    Saves an icon.
    """

    print(f"Writing: {filename}")
    tree.write(filename, encoding="utf-8", xml_declaration=False, method="xml")


def inkscape_clip(inkscape: str, filename: str) -> None:
    """
    Use inkscape to apply the clipping.
    """
    run([inkscape, filename,
         "--select", "path1,clip",  # Base path and clipping mask
         "--actions", f"path-difference;export-filename:{filename};export-plain-svg;export-do",
        ])


def scour(scour: str, filename: str) -> None:
    """
    Optimize with scour.
    """
    run([scour, filename, filename + ".tmp",
         "--enable-id-stripping", "--protect-ids-list=current-color-scheme",
         "--nindent", "4",
        ])
    os.replace(filename + ".tmp", filename)


def make_icon(base_name: str, with_charging: bool, with_profile: bool, output: str):
    """
    Produces an icon.
    """

    tree = etree.parse(base_name + ".svg")
    root = tree.getroot()
    if with_charging:
        # Style
        style = root.find(".//{http://www.w3.org/2000/svg}style")
        style.text += charging_style

    # Paths
    if with_profile:
        root.append(clip)
        path = root.find(".//{http://www.w3.org/2000/svg}path")
        # Standardize style
        profile.attrib["style"] = "fill:currentColor;fill-opacity:1;stroke:none"
        # Copy the class to the profile emblem so it shares the icon color
        profile.attrib["class"] = path.attrib["class"]

    if with_charging:
        c = copy(charging)
        root.append(c)

    if with_profile:
        # Translate the charging symbol if requested
        if with_charging and args.profile_translate_charging is not None:
            c.attrib["transform"] = f"translate({args.profile_translate_charging})"
        root.append(profile)

    save(tree, output)
    if with_profile:
        inkscape_clip(args.inkscape, output)
    scour(args.scour, output)


# These are needed to prevent nonsense namespaces like ns0 from being
# added to otherwise perfectly fine svg elements and attributes
etree.register_namespace("w3c", "http://www.w3.org/2000/svg")
etree.register_namespace("xlink", "http://www.w3.org/1999/xlink")
etree.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
etree.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
etree.register_namespace("cc", "http://creativecommons.org/ns#")
etree.register_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
etree.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

# Parse the command line
parser = argparse.ArgumentParser()
parser.add_argument("--charging", metavar="FILE", help="SVG with (only) the charging symbol")
parser.add_argument("--profile", metavar="NAME", help="Name of the power profile")
parser.add_argument("--profile-clip", metavar="FILE",
                    help="SVG with (only) the element to use for clipping the base icon "
                         "when showing profile information")
parser.add_argument("--profile-emblem", metavar="FILE",
                    help="SVG with (only) the element to add when showing profile information")
parser.add_argument("--profile-translate-charging", metavar="X,Y", default=None,
                    help="Translate the charging symbol when when drawing the profile")
parser.add_argument("--inkscape", default="inkscape", help="Inkscape command line")
parser.add_argument("--scour", default="scour", help="Scour command line")
parser.add_argument("inputs", metavar="FILE", nargs="+",
                    help="Base icons without charging indicators. Must contain a single path")
args = parser.parse_args()

# Load the charging symbol
charging = etree.parse(args.charging).find(".//{http://www.w3.org/2000/svg}path")
charging_style = etree.parse(args.charging).find(".//{http://www.w3.org/2000/svg}style").text

# Load the profile paths
clip = etree.parse(args.profile_clip).find(".//{http://www.w3.org/2000/svg}path")
clip.attrib["id"] = "clip"
profile = etree.parse(args.profile_emblem).find(".//{http://www.w3.org/2000/svg}path")

for f in args.inputs:
    base_name, _ = os.path.splitext(f)
    # Uncomment if you want to make new -charging icons as well
    #make_icon(base_name, True, False, f"{base_name}-charging.svg")
    make_icon(base_name, False, True, f"{base_name}-profile-{args.profile}.svg")
    make_icon(base_name, True,  True, f"{base_name}-charging-profile-{args.profile}.svg")
