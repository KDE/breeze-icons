/*
    Copyright 2021 Hannah von Reth <vonreth@kde.org>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) version 3, or any
    later version accepted by the membership of KDE e.V. (or its
    successor approved by the membership of KDE e.V.), which shall
    act as a proxy defined in Section 6 of version 3 of the license.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library. If not, see <http://www.gnu.org/licenses/>.
*/

#include <QDirIterator>
#include <QObject>
#include <QTest>
#include <QResource>
#include <QScopeGuard>
#include <QCryptographicHash>

#include "testhelpers.h"

class TestRcc : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void initTestCase_data() {
        QTest::addColumn<QString>("theme");
        for (const auto &theme : QStringList{ICON_DIRS}) {
            QTest::newRow(theme.toUtf8().data()) << theme;
            break; // dark isn't generated yet
        }
    }
    
    void initTestCase()
    {
        // Go up one level from the bin dir
        m_buildDir = QDir(QCoreApplication::applicationDirPath() + "/..").canonicalPath();
    }

    void test_rcc()
    {
        QFETCH_GLOBAL(QString, theme);
        const QString root = QStringLiteral("/rcc");
        const QString themePath = QStringLiteral("%1/icons/breeze-%2.rcc").arg(m_buildDir, theme);
        QVERIFY(QResource::registerResource(themePath, root));
        auto cleanup = qScopeGuard([=]{
            QVERIFY(QResource::unregisterResource(themePath, root));
        });
        const QDir srcDir = QStringLiteral(PROJECT_SOURCE_DIR "/%1").arg(theme);
        QDirIterator it(srcDir.path(), {"*.svg"}, QDir::Files, QDirIterator::Subdirectories | QDirIterator::FollowSymlinks);
        while (it.hasNext()) {
            it.next();
            const auto info = it.fileInfo();
            QFile file(info.filePath());
            QFile resource(QStringLiteral(":%1/%2").arg(root, srcDir.relativeFilePath(info.filePath())));

            QVERIFY(file.open(QFile::ReadOnly));
            QVERIFY(resource.open(QFile::ReadOnly));
            
            QCryptographicHash fileHash(QCryptographicHash::Md5);
            QVERIFY(fileHash.addData(&file)); 
            QCryptographicHash resourceHash(QCryptographicHash::Md5);
            QVERIFY(resourceHash.addData(&resource));
            QCOMPARE(fileHash.result().toHex(), resourceHash.result().toHex());
        }
    }

private:
    QString m_buildDir;
};

QTEST_GUILESS_MAIN(TestRcc)

#include "testrcc.moc"
