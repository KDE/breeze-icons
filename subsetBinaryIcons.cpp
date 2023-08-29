/* This file is part of the KDE libraries
 * SPDX-FileCopyrightText: 2016 Kåre Särs <kare.sars@iki.fi>
 * SPDX-FileCopyrightText: 2023 g10 Code GmbH
 * SPDX-FileContributor: Sune Stolborg Vuorela <sune@vuorela.dk>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */
#include <QCommandLineParser>
#include <QCoreApplication>
#include <QDebug>
#include <QFile>
#include <QFileInfo>
#include <QRegularExpression>
#include <QString>

int parseFile(const QString &infile, const QString &outfile, const QStringList &includeFilter)
{
    QFile in(infile);
    QFile out(outfile);
    static QRegularExpression imageReg(QStringLiteral("<file>(.*\\.(?:svg|png|gif|ico))</file>"));

    if (!in.open(QIODevice::ReadOnly)) {
        qWarning() << "Failed to open" << infile;
        return -1;
    }
    if (!out.open(QIODevice::WriteOnly)) {
        qWarning() << "Failed to create" << outfile;
        return -2;
    }

    while (in.bytesAvailable()) {
        const QString line = QString::fromLocal8Bit(in.readLine());
        const QRegularExpressionMatch match = imageReg.match(line);
        if (!match.hasMatch()) {
            // qDebug() << "No Match: " << line;
            out.write(qPrintable(line));
            continue;
        }

        const QFileInfo info(match.captured(1));
        if (!includeFilter.contains(info.completeBaseName())) {
            continue;
        }
        out.write(qPrintable(line));
    }
    return 0;
}

static QStringList parseIncludeList(const QString &path)
{
    QStringList items;
    QFile in(path);
    if (!in.open(QIODevice::ReadOnly)) {
        qWarning() << "failed to open" << path;
        return {};
    }
    while (in.bytesAvailable()) {
        const QString line = QString::fromLocal8Bit(in.readLine()).trimmed();
        if (line.startsWith(QLatin1Char('#'))) {
            continue;
        }
        items.push_back(line);
    }
    return items;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QCommandLineParser parser;

    QCommandLineOption inOption({ QLatin1String("i"), QLatin1String("infile") }, QStringLiteral("Input qrc file"), QStringLiteral("infile"));
    QCommandLineOption outOption({ QLatin1String("o"), QLatin1String("outfile") }, QStringLiteral("Output qrc file"), QStringLiteral("outfile"));
    QCommandLineOption includeOption({ QLatin1String("I"), QLatin1String("include") },
                                     QStringLiteral("InputFilter list (newline delimited, no extensions)"),
                                     QStringLiteral("include"));
    parser.setApplicationDescription(
        QLatin1String("Utility to help just include some icons and not a full icon set."
                      "This is a singleapplication distributino helper for power users; proceed at own risk"));
    parser.addHelpOption();
    parser.addVersionOption();
    parser.addOption(inOption);
    parser.addOption(outOption);
    parser.addOption(includeOption);
    parser.process(app);

    const QString inName = parser.value(inOption);
    const QString outName = parser.value(outOption);
    if (!parser.isSet(includeOption)) {
        auto ret = QFile::copy(inName, outName);
        if (ret) {
            return 0;
        } else {
            return 1;
        }
    }

    const QStringList includeFilters = parseIncludeList(parser.value(includeOption));
    if (includeFilters.empty()) {
        return 1;
    }

    return parseFile(inName, outName, includeFilters);
}
