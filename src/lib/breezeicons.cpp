/*
    This file is part of the KDE libraries

    SPDX-FileCopyrightText: 2021 Christoph Cullmann <cullmann@kde.org>

    SPDX-License-Identifier: LGPL-2.0-or-later
*/

#include "breezeicons.h"

#include <QIcon>

namespace BreezeIcons
{

void initIcons()
{
    // ensure we fallback to breeze
    QIcon::setFallbackThemeName(QStringLiteral("breeze"));
}

}
