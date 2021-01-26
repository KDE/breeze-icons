/*
    This file is part of the KDE libraries

    SPDX-FileCopyrightText: 2021 Christoph Cullmann <cullmann@kde.org>

    SPDX-License-Identifier: LGPL-2.0-or-later
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
