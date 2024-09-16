/*
    SPDX-FileCopyrightText: 2015-2016 Harald Sitter <sitter@kde.org>

    SPDX-License-Identifier: LGPL-2.1-only OR LGPL-3.0-only OR LicenseRef-KDE-Accepted-LGPL
*/

#ifndef TESTHELPERS_H
#define TESTHELPERS_H

#include <QFileInfo>
#include <QList>
#include <QString>

#include "testdata.h"

#define _T_LIST_INDENT QStringLiteral("  ")
#define _T_LIST_INDENT2 QStringLiteral("    ")

void failListContent(const QList<QString> &list, const QString &header)
{
    if (list.empty()) {
        return;
    }
    QString message = (QStringLiteral("\n") + _T_LIST_INDENT + header);
    for (const auto& path : list) {
        message += (_T_LIST_INDENT2 + QStringLiteral("- ") + path + QStringLiteral("\n"));
    }
    QFAIL(qPrintable(message));
}

void failSymlinkList(const QList<QFileInfo> &list, const QString &header)
{
    if (list.empty()) {
        return;
    }
    QString message = (QStringLiteral("\n") + _T_LIST_INDENT + header);
    for (const auto& info : list) {
        message += (_T_LIST_INDENT2 + info.filePath() + QStringLiteral(" => ") + info.symLinkTarget() + QStringLiteral("\n"));
    }
    QFAIL(qPrintable(message));
}

#endif // TESTHELPERS_H
