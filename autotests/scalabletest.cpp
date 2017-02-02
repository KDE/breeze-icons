/*
    Copyright 2017 Harald Sitter <sitter@kde.org>

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

#include <QObject>
#include <QtTest>

#include <KConfig>
#include <KConfigGroup>
#include <KIconLoader>

#include "testhelpers.h"

/**
 * Represents icon directory to conduct simple icon lookup within.
 */
class Dir
{
public:
    Dir(const KConfigGroup &cg, const QString &themeDir_)
        : exists(checkExist(cg))
        , themeDir(themeDir_)
        , path(cg.name())
        , size(cg.readEntry("Size", 0))
        , contextString(cg.readEntry("Context", QString()))
        , context(parseContext(contextString))
        , type(parseType(cg.readEntry("Type", QString("Threshold"))))
    {
        QVERIFY2(context != -1,
                 QString("Don't know how to handle 'Context=%1' of config group '[%2]'").arg(contextString, cg.name()).toLatin1());
    }

    static void verify(const KConfigGroup &cg)
    {
        QVERIFY2(cg.exists(),
                 QString("The theme's 'Directories' specifies '%1' as directory which appears to"
                         " have no associated group entry '[%1]'").arg(cg.name()).toLatin1());
    }

    static bool checkExist(const KConfigGroup &cg)
    {
        verify(cg); // extra func since QVERIFY2 is a return
        return cg.isValid();
    }

    static QMetaEnum findEnum(const char *name)
    {
        auto mo = KIconLoader::staticMetaObject;
        for (int i = 0; i < mo.enumeratorCount(); ++i) {
            auto enumerator = mo.enumerator(i);
            if (strcmp(enumerator.name(), name) == 0) {
                return KIconLoader::staticMetaObject.enumerator(i);
            }
        }
        Q_ASSERT(false); // failed to resolve enum
        return QMetaEnum();
    }

    static QMetaEnum typeEnum()
    {
        static auto e = findEnum("Type");
        return e;
    }

    KIconLoader::Context parseContext(const QString &string)
    {
        // Can't use QMetaEnum as the enum names are singular, the entry values are plural though.
        static QHash<QString, int> hash {
            { QStringLiteral("Actions"), KIconLoader::Action },
            { QStringLiteral("Applications"), KIconLoader::Application },
            { QStringLiteral("Categories"), KIconLoader::Category },
            { QStringLiteral("Devices"), KIconLoader::Device },
            { QStringLiteral("Emblems"), KIconLoader::Emblem },
            { QStringLiteral("Emotes"), KIconLoader::Emote },
            { QStringLiteral("MimeTypes"), KIconLoader::MimeType },
            { QStringLiteral("Places"), KIconLoader::Place },
            { QStringLiteral("Status"), KIconLoader::StatusIcon },
        };
        auto value = hash.value(string, -1);
        return (KIconLoader::Context)value;
    }

    KIconLoader::Type parseType(const QString &string)
    {
        bool ok;
        auto v = (KIconLoader::Type)typeEnum().keyToValue(string.toLatin1(), &ok);
        Q_ASSERT(ok);
        return v;
    }

    /**
     * @returns list of all icon's fileinfo (first level only, selected types
     *          only)
     */
    QList<QFileInfo> allIcons()
    {
        QList<QFileInfo> icons;
        auto iconDir = QString("%1/%2").arg(themeDir).arg(path);
        QDirIterator it(iconDir);
        while (it.hasNext()) {
            it.next();
            auto suffix = it.fileInfo().suffix();
            if (suffix != "svg" && suffix != "svgz" && suffix != "png") {
                continue; // Probably not an icon.
            }
            icons << it.fileInfo();
        }
        return icons;
    }

    bool exists;
    QString themeDir;
    QString path;
    uint size;
    QString contextString;
    KIconLoader::Context context;
    KIconLoader::Type type;
};

// Declare so we can put them into the QTest data table.
Q_DECLARE_METATYPE(KIconLoader::Context)
Q_DECLARE_METATYPE(Dir*)

class ScalableTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    // NB: test_scalable_data leaks Dir*. Should this test grow more slots it may be wise to
    //     introduce a cleanup() to make sure the test doesn't OOM.

    void test_scalable_data()
    {
        for (auto dir : ICON_DIRS) {
            auto themeDir = PROJECT_SOURCE_DIR + QStringLiteral("/") + dir;

            QHash<KIconLoader::Context, QList<Dir *>> contextHash;
            QHash<KIconLoader::Context, QString> contextStringHash;

            KConfig config(themeDir + "/index.theme");
            auto directoryPaths = config.group("Icon Theme").readEntry("Directories", QString()).split(",");
            QVERIFY(!directoryPaths.isEmpty());
            for (auto directoryPath : directoryPaths) {
                auto dir = new Dir(config.group(directoryPath), themeDir);
                contextHash[dir->context].append(dir);
                contextStringHash[dir->context] = (dir->contextString);
            }

            QTest::addColumn<KIconLoader::Context>("context");
            QTest::addColumn<QList<Dir *>>("dirs");

            for (auto key : contextHash.keys()) {
                if (key != KIconLoader::Application) {
                    qDebug() << "Only testing Application context for now.";
                    continue;
                }
                // FIXME: go through qenum to stringify the bugger
                // Gets rid of the stupid second hash
                auto contextId = QString(QLatin1String(dir) + ":" + contextStringHash[key]).toLatin1();
                QTest::newRow(contextId) << key << contextHash[key];
            }
        }
    }

    void test_scalable()
    {
        QFETCH(KIconLoader::Context, context);
        QFETCH(QList<Dir *>, dirs);

        QList<Dir *> fixedDirs;
        QList<Dir *> scalableDirs;
        for (auto dir : dirs) {
            switch (dir->type) {
            case KIconLoader::Scalable:
                scalableDirs << dir;
                break;
            case KIconLoader::Fixed:
                fixedDirs << dir;
                break;
            case KIconLoader::Threshold:
                QVERIFY2(false, "Test does not support threshold icons right now.");
            }
        }

        // FIXME: context should be translated through qenum
        switch (context) {
        case KIconLoader::Application:
            // Treat this as a problem.
            QVERIFY2(!scalableDirs.empty(), "This icon context has no scalable directory at all!");
            break;
        default:
            qWarning() << "All context but Application are whitelisted from having a scalable directory.";
            return;
        }

        QStringList fixedIcons;
        for (auto dir : fixedDirs) {
            for (auto iconInfo : dir->allIcons()) {
                fixedIcons << iconInfo.completeBaseName();
            }
        }

        QHash<QString, QList<QFileInfo>> scalableIcons;
        for (auto dir : scalableDirs) {
            for (auto iconInfo : dir->allIcons()) {
                scalableIcons[iconInfo.completeBaseName()].append(iconInfo);
            }
        }

        QStringList notScalableIcons;
        for (auto fixed : fixedIcons) {
            if (scalableIcons.keys().contains(fixed)) {
                continue;
            }
            notScalableIcons << fixed;
        }

        // Assert that each icon has a scalable variant.
        if (notScalableIcons.empty()) {
            return;
        }
        notScalableIcons.removeDuplicates();
        QFAIL(QString("The following icons are not available in a scalable directory:\n  %1")
              .arg(notScalableIcons.join("\n  "))
              .toLatin1());
    }

    void test_scalableDuplicates_data()
    {
        test_scalable_data();
    }

    void test_scalableDuplicates()
    {
        QFETCH(QList<Dir *>, dirs);

        QList<Dir *> scalableDirs;
        for (auto dir : dirs) {
            switch (dir->type) {
            case KIconLoader::Scalable:
                scalableDirs << dir;
                break;
            case KIconLoader::Fixed:
                // Not of interest in this test.
                break;
            case KIconLoader::Threshold:
                QVERIFY2(false, "Test does not support threshold icons right now.");
            }
        }

        QHash<QString, QList<QFileInfo>> scalableIcons;
        for (auto dir : scalableDirs) {
            for (auto iconInfo : dir->allIcons()) {
                scalableIcons[iconInfo.completeBaseName()].append(iconInfo);
            }
        }

        QHash<QString, QList<QFileInfo>> duplicatedScalableIcons;
        for (auto icon: scalableIcons.keys()) {
            auto list = scalableIcons[icon];
            if (list.size() > 1) {
                duplicatedScalableIcons[icon] = list;
            }
        }

        // Assert that there is only one scalable version per icon name.
        // Otherwise apps/32/klipper.svg OR apps/48/klipper.svg may be used.
        if (!duplicatedScalableIcons.empty()) {
            QString msg;
            QTextStream stream(&msg);
            stream << "Duplicated scalable icons:" << endl;
            for (auto icon : duplicatedScalableIcons.keys()) {
                stream << QString("  %1:").arg(icon) << endl;
                for (auto info : duplicatedScalableIcons[icon]) {
                    stream << QString("    %1").arg(info.absoluteFilePath()) << endl;
                }
            }
            QFAIL(msg.toLatin1());
        }
    }
};

QTEST_GUILESS_MAIN(ScalableTest)

#include "scalabletest.moc"
