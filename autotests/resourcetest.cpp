/*
    This file is part of the KDE libraries

    SPDX-FileCopyrightText: 2025 Christoph Cullmann <cullmann@kde.org>

    SPDX-License-Identifier: LGPL-2.0-or-later
*/

#include <QFile>
#include <QObject>
#include <QTest>

#include "breezeicons.h"
#include "testhelpers.h"

class ResourceTest : public QObject
{
    Q_OBJECT

    void compareFileResourceWithFilesystem(const QString &name)
    {
        // resource location
        const QString qrcLocation(QStringLiteral(":/icons/breeze/%1").arg(name));

        // file system location
        const QString fsLocation(PROJECT_SOURCE_DIR + QStringLiteral("/icons/%1").arg(name));

        // read full data of both, must work
        QFile qrcFile(qrcLocation);
        QVERIFY(qrcFile.open(QFile::ReadOnly));
        QFile fsFile(fsLocation);
        QVERIFY(fsFile.open(QFile::ReadOnly));
        const auto qrcData = qrcFile.readAll();
        QVERIFY(!qrcData.isEmpty());
        const auto fsData = fsFile.readAll();
        QVERIFY(!fsData.isEmpty());

        // fully equal?
        QCOMPARE(qrcData, fsData);
    }

private Q_SLOTS:
    // check that not stuff got lost in the DLL
    // did happen for compiling with LTO or buggy preprocessing the DLL
    void test_resourceContainsTheme()
    {
        // ensure the DLL is linked
        BreezeIcons::initIcons();

        // we want to have the proper theme file
        compareFileResourceWithFilesystem(QStringLiteral("index.theme"));

        // check some icons we know shall be there
        // check no stuff that might not be generated in some config or that is a symlink
        compareFileResourceWithFilesystem(QStringLiteral("actions/16/go-previous.svg"));
        compareFileResourceWithFilesystem(QStringLiteral("actions/16/table.svg"));
        compareFileResourceWithFilesystem(QStringLiteral("actions/22/edit-paste.svg"));
        compareFileResourceWithFilesystem(QStringLiteral("actions/22/tab-new.svg"));
        compareFileResourceWithFilesystem(QStringLiteral("actions/32/document-edit.svg"));
        compareFileResourceWithFilesystem(QStringLiteral("actions/32/zoom.svg"));
        compareFileResourceWithFilesystem(QStringLiteral("mimetypes/64/application-json.svg"));
        compareFileResourceWithFilesystem(QStringLiteral("places/64/folder-favorites.svg"));
    }
};

QTEST_GUILESS_MAIN(ResourceTest)

#include "resourcetest.moc"
