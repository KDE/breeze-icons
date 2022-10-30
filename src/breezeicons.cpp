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

    // enforce theme + fallback theme
    QIcon::setFallbackThemeName(themeName);
    QIcon::setThemeName(themeName);
}

// stored connection for later disconnect in deinitIcons
Q_GLOBAL_STATIC(QMetaObject::Connection, updateConnection)

namespace BreezeIcons
{

void initIcons()
{
    // we require a gui application instance
    Q_ASSERT(qGuiApp);

    // once update theme manually
    updateThemeForPalette(qGuiApp->palette());
    printf("lslslslslslslsafn\n");

    // register for later changes
    *updateConnection() = QObject::connect(qGuiApp, &QGuiApplication::paletteChanged, &updateThemeForPalette);
}

void deinitIcons()
{
    // if we have no gui application or no connection setup => nop
    if (!qGuiApp || !(*updateConnection())) {
        return;
    }

    // unregister theme update function to allow again other themes to be used without interference
    QObject::disconnect(*updateConnection());
}

}
