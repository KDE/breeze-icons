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
 * Sets up the Breeze icons and sets the icon theme used by Qt
 * to the Breeze icons.
 *
 * This automatically switches between Breeze light and Breeze dark
 * based on the base color of your application's palette, and listens
 * to changes to the application's palette and switches between the
 * icon themes accordingly.
 *
 * Call this function after having constructed your QGuiApplication or
 * QApplication.
 *
 * @warning Calling this function before a QGuiApplication has been constructed
 * will likely cause a crash.
 */
BREEZEICONS_EXPORT void initIcons();

/**
 * Deactivates the automatic switching between Breeze light and Breeze dark
 * as activated with initIcons again.
 */
BREEZEICONS_EXPORT void deinitIcons();

}

#endif
