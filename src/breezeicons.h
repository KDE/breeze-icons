/*
    This file is part of the KDE libraries

    SPDX-FileCopyrightText: 2021 Christoph Cullmann <cullmann@kde.org>

    SPDX-License-Identifier: LGPL-2.0-or-later
*/

#ifndef BREEZEICONS_H
#define BREEZEICONS_H

#include <breezeicons_export.h>

/**
 * This namespace contains utility functions to integrate the
 * Breeze icons into your application.
 */
namespace BreezeIcons
{

/**
 * Ensure the Breeze icons as bundled as resources inside this
 * library are used by the application.
 *
 * Call this function after your QGuiApplication is constructed.
 *
 * It will both set the right icon theme for Qt and ensure
 * that palette changes are handled to switch between light
 * and dark icons.
 */
BREEZEICONS_EXPORT void initIcons();

}

#endif
