/*
    This file is part of the KDE libraries

    SPDX-FileCopyrightText: 2021 Christoph Cullmann <cullmann@kde.org>

    SPDX-License-Identifier: LGPL-2.0-or-later
*/

#include "breezeicons.h"

#include <QIcon>

static void resourceInit()
{
    // needs to be called outside of namespace
    Q_INIT_RESOURCE(breeze_icons);
}

namespace BreezeIcons
{

void initIcons()
{
    // ensure the resource is there and loaded for static libs
    resourceInit();

    // ensure we fallback to breeze, if no user fallback is set
    const QString fallbackTheme = QIcon::fallbackThemeName();
    if (fallbackTheme.isEmpty() || fallbackTheme == QLatin1String("hicolor")) {
        QIcon::setFallbackThemeName(QStringLiteral("breeze"));
    }
}

}
