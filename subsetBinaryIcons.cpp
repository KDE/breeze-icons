/*  This file is part of the KDE libraries
 *    Copyright (C) 2016 Kåre Särs <kare.sars@iki.fi>
 *
 *     SPDX-FileCopyrightText: 2023 g10 Code GmbH
 *     SPDX-FileContributor: Sune Stolborg Vuorela <sune@vuorela.dk>
 *
 *    This library is free software; you can redistribute it and/or
 *    modify it under the terms of the GNU Library General Public
 *    License as published by the Free Software Foundation; either
 *    version 2 of the License, or (at your option) any later version.
 *
 *    This library is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *    Library General Public License for more details.
 *
 *    You should have received a copy of the GNU Library General Public License
 *    along with this library; see the file COPYING.LIB.  If not, write to
 *    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 *    Boston, MA 02110-1301, USA.
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
    QRegularExpression imageReg(QStringLiteral("<file>(.*\\.(?:svg|png|gif|ico))</file>"));

    if (!in.open(QIODevice::ReadOnly)) {
        qDebug() << "Failed to open" << infile;
        return -1;
    }
    if (!out.open(QIODevice::WriteOnly)) {
        qDebug() << "Failed to create" << outfile;
        return -2;
    }

    while (in.bytesAvailable()) {
        QString line = QString::fromLocal8Bit(in.readLine());
        QRegularExpressionMatch match = imageReg.match(line);
        if (!match.hasMatch()) {
            // qDebug() << "No Match: " << line;
            out.write(qPrintable(line));
            continue;
        }

        QFileInfo info(match.captured(1));
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
        qDebug() << "failed to open" << path;
        return {};
    }
    while (in.bytesAvailable()) {
        QString line = QString::fromLocal8Bit(in.readLine()).trimmed();
        if (line.startsWith(QStringLiteral("#"))) {
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

    QCommandLineOption inOption(QStringList() << QLatin1String("i") << QLatin1String("infile"), QStringLiteral("Input qrc file"), QStringLiteral("infile"));
    QCommandLineOption outOption(QStringList() << QLatin1String("o") << QLatin1String("outfile"), QStringLiteral("Output qrc file"), QStringLiteral("outfile"));
    QCommandLineOption includeOption(QStringList() << QLatin1String("I") << QLatin1String("include"),
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
