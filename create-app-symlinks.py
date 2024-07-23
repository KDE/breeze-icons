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
    "anydesk": ["com.anydesk.Anydesk"],
    "ardour": ["org.ardour.Ardour"],
    "ark": ["org.kde.ark"],
    "artikulate": ["org.kde.artikulate"],
    "atom": ["io.atom.Atom"],
    "audacity": ["org.audacityteam.Audacity"],
    "blender": ["org.blender.Blender"],
    "blinken": ["org.kde.blinken"],
    "bluefish": ["nl.openoffice.bluefish"],
    "bomber": ["org.kde.bomber"],
    "bovo": ["org.kde.bovo"],
    "brackets": ["io.brackets.Brackets"],
    "cantor": ["org.kde.cantor"],
    "claws-mail": ["org.claws_mail.Claws-Mail"],
    "converseen": ["net.fasterland.converseen"],
    "crow-translate": ["org.kde.CrowTranslate.svg"],
    "darktable": ["org.darktable.Darktable"],
    "diffuse": ["io.github.mightycreak.Diffuse"],
    "digikam": ["org.kde.digikam"],
    "elisa": ["org.kde.elisa"],
    "falkon": ["org.kde.falkon"],
    "filezilla": ["org.filezillaproject.Filezilla"],
    "fontforge": ["org.fontforge.FontForge"],
    "gimp": ["org.gimp.GIMP"],
    "git-cola": ["com.github.git_cola.git-cola"],
    "goodvibes": ["io.gitlab.Goodvibes"],
    "gpodder": ["org.gpodder.gpodder"],
    "granatier": ["org.kde.granatier"],
    "gtkhash": ["org.gtkhash.gtkhash"],
    "gwenview": ["org.kde.gwenview"],
    "haguichi": ["com.github.ztefn.haguichi"],
    "handbrake": ["fr.handbrake.ghb"],
    "homebank": ["fr.free.Homebank"],
    "inkscape": ["org.inkscape.Inkscape"],
    "jdownloader": ["org.jdownloader.JDownloader"],
    "joplin": ["net.cozic.joplin_desktop"],
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
    "leocad": ["org.leocad.LeoCAD"],
    "libreoffice-base": ["org.libreoffice.LibreOffice.base"],
    "libreoffice-calc": ["org.libreoffice.LibreOffice.calc"],
    "libreoffice-draw": ["org.libreoffice.LibreOffice.draw"],
    "libreoffice-impress": ["org.libreoffice.LibreOffice.impress"],
    "libreoffice-math": ["org.libreoffice.LibreOffice.math"],
    "libreoffice-startcenter": ["org.libreoffice.LibreOffice.startcenter"],
    "libreoffice-writer": ["org.libreoffice.LibreOffice.writer"],
    "lokalize": ["org.kde.lokalize"],
    "massif-visualizer": ["org.kde.massif-visualizer"],
    "masterpdfeditor": ["net.codeindustry.MasterPDFEditor"],
    "mendeleydesktop": ["com.elsevier.MendeleyDesktop"],
    "minitube": ["org.tordini.flavio.Minitube"],
    "minuet": ["org.kde.minuet"],
    "mpv": ["io.mpv.Mpv"],
    "nota": ["org.kde.nota"],
    "okteta": ["org.kde.okteta"],
    "okular": ["org.kde.okular"],
    "picmi": ["org.kde.picmi"],
    "q4wine": ["ua.org.brezblock.q4wine"],
    "qbittorrent": ["org.qbittorrent.qBittorrent"],
    "qelectrotech": ["org.qelectrotech.QElectroTech"],
    "rosegarden": ["com.rosegardenmusic.rosegarden"],
    "scribus": ["net.scribus.Scribus"],
    "skanlite": ["org.kde.skanlite"],
    "skrooge": ["org.kde.skrooge"],
    "smartgit": ["com.syntevo.SmartGit"],
    "smplayer": ["info.smplayer.SMPlayer"],
    "steam": ["com.valvesoftware.Steam"],
    "sublime-merge": ["com.sublimemerge.App"],
    "sublime-text": ["com.sublimetext.Three"],
    "telegram": ["org.telegram.desktop"],
    "texstudio": ["org.texstudio.TeXstudio"],
    "umbrello": ["org.kde.umbrello"],
    "viber": ["com.viber.Viber"],
    "vlc": ["org.videolan.VLC"],
    "vvave": ["org.kde.vvave"],
    "wine": ["org.winehq.Wine"],
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
