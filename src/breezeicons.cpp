/*  SPDX-License-Identifier: LGPL-2.0-or-later

    Copyright (C) 2019 Christoph Cullmann <cullmann@kde.org>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public License
    along with this library; see the file COPYING.LIB.  If not, write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1301, USA.
*/

#include "breezeicons.h"

#include <QGuiApplication>
#include <QIcon>
#include <QPalette>

/**
 * Set right theme for given palette
 * @param palette palette to derive theme from
 */
static void updateThemeForPalette(const QPalette &palette)
{
    // decide if we want normal or dark theme based on application palette
    const auto darkTheme = palette.color(QPalette::Base).lightness() < 128;
    const auto themeName = darkTheme ? QStringLiteral("breeze-dark") : QStringLiteral("breeze");

    // just enforce theme + fallback theme, allowing the users to overwrite this
    QIcon::setFallbackThemeName(themeName);
    QIcon::setThemeName(themeName);
}

namespace BreezeIcons
{

void initIcons()
{
    // we require a gui application instance
    Q_ASSERT(qGuiApp);

    // once update theme manually
    updateThemeForPalette(qGuiApp->palette());

    // register for later changes
    QObject::connect(qGuiApp, &QGuiApplication::paletteChanged, &updateThemeForPalette);
}

}
