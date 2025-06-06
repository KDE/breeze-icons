#!/usr/bin/env python3

"""
SPDX-License-Identifier: LGPL-2.1-only OR LGPL-3.0-only OR LicenseRef-KDE-Accepted-LGPL
SPDX-FileCopyrightText: 2022 Alois Wohlschlager <alois1@gmx-topmail.de>
"""

from pprint import pprint
import os
import shutil
import sys

aliases = {
    "akregator": ["org.kde.akregator"],
    "alligator": ["org.kde.alligator"],
    "amarok": ["org.kde.amarok"],
    "ark": ["org.kde.ark"],
    "artikulate": ["org.kde.artikulate"],
    "blinken": ["org.kde.blinken"],
    "bomber": ["org.kde.bomber"],
    "bovo": ["org.kde.bovo"],
    "cantor": ["org.kde.cantor"],
    "crow-translate": ["org.kde.CrowTranslate.svg"],
    "cuttlefish": ["org.kde.iconexplorer"],
    "digikam": ["org.kde.digikam"],
    "elisa": ["org.kde.elisa"],
    "falkon": ["org.kde.falkon"],
    "granatier": ["org.kde.granatier"],
    "gwenview": ["org.kde.gwenview"],
    "juk": ["org.kde.juk"],
    "kalgebra": ["org.kde.kalgebra"],
    "kalzium": ["org.kde.kalzium"],
    "kamoso": ["org.kde.kamoso"],
    "kanagram": ["org.kde.kanagram"],
    "kapman": ["org.kde.kapman"],
    "katomic": ["org.kde.katomic"],
    "kblackbox": ["org.kde.kblackbox"],
    "kblocks": ["org.kde.kblocks"],
    "kbreakout": ["org.kde.kbreakout"],
    "kbruch": ["org.kde.kbruch"],
    "kcachegrind": ["org.kde.kcachegrind"],
    "kcolorchooser": ["org.kde.kcolorchooser"],
    "kdenlive": ["org.kde.kdenlive"],
    "kdevelop": ["org.kde.kdevelop"],
    "kdiamond": ["org.kde.kdiamond"],
    "kdiff3": ["org.kde.kdiff3"],
    "kfind": ["org.kde.kfind"],
    "kfourinline": ["org.kde.kfourinline"],
    "kgeography": ["org.kde.kgeography"],
    "kget": ["org.kde.kget"],
    "khangman": ["org.kde.khangman"],
    "kig": ["org.kde.kig"],
    "kile": ["org.kde.kile"],
    "kiriki": ["org.kde.kiriki"],
    "kiten": ["org.kde.kiten"],
    "kjumpingcube": ["org.kde.kjumpingcube"],
    "kmplot": ["org.kde.kmplot"],
    "knights": ["org.kde.knights"],
    "kolf": ["org.kde.kolf"],
    "kolourpaint": ["org.kde.kolourpaint"],
    "kontact": ["org.kde.kontact"],
    "konversation": ["org.kde.konversation"],
    "kopete": ["org.kde.kopete"],
    "kpat": ["org.kde.kpat"],
    "kphotoalbum": ["org.kde.kphotoalbum"],
    "krdc": ["org.kde.krdc"],
    "krename": ["org.kde.krename"],
    "kronometer": ["org.kde.kronometer"],
    "kruler": ["org.kde.kruler"],
    "ksirk": ["org.kde.ksirk"],
    "kstars": ["org.kde.kstars"],
    "kteatime": ["org.kde.kteatime"],
    "ktimetracker": ["org.kde.ktimetracker"],
    "ktorrent": ["org.kde.ktorrent"],
    "ktouch": ["org.kde.ktouch"],
    "ktrip": ["org.kde.ktrip"],
    "kuiviewer": ["org.kde.kuiviewer"],
    "kwrite": ["org.kde.kwrite"],
    "kxstitch": ["org.kde.kxstitch"],
    "kwalletmanager": ["org.kde.kwalletmanager5"],
    "labplot": ["org.kde.labplot2"],
    "lokalize": ["org.kde.lokalize"],
    "massif-visualizer": ["org.kde.massif-visualizer"],
    "minuet": ["org.kde.minuet"],
    "nota": ["org.kde.nota"],
    "okteta": ["org.kde.okteta"],
    "okular": ["org.kde.okular"],
    "picmi": ["org.kde.picmi"],
    "skanlite": ["org.kde.skanlite"],
    "skrooge": ["org.kde.skrooge"],
    "umbrello": ["org.kde.umbrello"],
    "vvave": ["org.kde.vvave"],
}

SRCDIR = sys.argv[1]
BINDIR = sys.argv[2]

shutil.rmtree(BINDIR, ignore_errors=True)

created_symlinks = dict()

for dirpath, _, filenames in os.walk(os.path.join(SRCDIR, "apps")):
    outpath = os.path.join(BINDIR + dirpath[len(SRCDIR):])
    os.makedirs(outpath)
    for file in filenames:
        if file[-4:] == ".svg":
            base = file[:-4]
            if base not in created_symlinks.keys():
                created_symlinks[base] = dict()
            if base in aliases:
                for alias in aliases[base]:
                    os.symlink(file, os.path.join(outpath, alias + ".svg"))
                    if alias not in created_symlinks[base].keys():
                        created_symlinks[base][alias] = []
                    created_symlinks[base][alias].append(int(outpath.split('/')[-1]))

print('Symlinking application icons to their Flatpak IDs:')
pprint(created_symlinks)
