/*
 * SPDX-FileCopyrightText: 2016 Kåre Särs <kare.sars@iki.fi>
 * SPDX-FileCopyrightText: 2024 Christoph Cullmann <cullmann@kde.org>
 *
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#include <QCommandLineParser>
#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QDirIterator>
#include <QFile>
#include <QFileInfo>
#include <QHash>
#include <QRegularExpression>
#include <QSet>
#include <QString>
#include <QXmlStreamReader>

/**
 * Check if this file is a duplicate of an other on, dies then.
 * @param fileName file to check
 */
static void checkForDuplicates(const QString &fileName)
{
    // get full content for dupe checking
    QFile in(fileName);
    if (!in.open(QIODevice::ReadOnly)) {
        qFatal() << "failed to open" << in.fileName() << "for XML validation";
    }

    // simplify content to catch files that just have spacing diffs
    // that should not matter for SVGs
    const auto fullContent = QString::fromUtf8(in.readAll()).simplified();

    // see if we did have this content already and die
    static QHash<QString, QString> contentToFileName;
    if (const auto it = contentToFileName.find(fullContent); it != contentToFileName.end()) {
        qFatal() << "file" << fileName << "is a duplicate of file" << it.value();
    }
    contentToFileName.insert(fullContent, fileName);
}

/**
 * Validate the XML, dies on errors.
 * @param fileName file to validate
 */
static void validateXml(const QString &fileName)
{
    // read once and bail out on errors
    QFile in(fileName);
    if (!in.open(QIODevice::ReadOnly)) {
        qFatal() << "failed to open" << in.fileName() << "for XML validation";
    }
    QXmlStreamReader xml(&in);
    while (!xml.atEnd()) {
        xml.readNext();
    }
    if (xml.hasError()) {
        qFatal() << "XML error " << xml.errorString() << "in file" << in.fileName() << "at line" << xml.lineNumber();
    }
}

/**
 * Given a dir and a file inside, resolve the pseudo symlinks we get from Git on Windows.
 * Does some consistency checks, will die if they fail.
 *
 * @param path directory that contains the given file
 * @param fileName file name of the dir to check if it is a pseudo link
 * @return target of the link or empty string if no link
 */
static QString resolveWindowsGitLink(const QString &path, const QString &fileName)
{
    QFile in(path + QLatin1Char('/') + fileName);
    if (!in.open(QIODevice::ReadOnly)) {
        qFatal() << "failed to open" << path << fileName << in.fileName();
    }

    QString firstLine = QString::fromLocal8Bit(in.readLine());
    if (firstLine.isEmpty()) {
        return QString();
    }
    QRegularExpression fNameReg(QStringLiteral("(.*\\.(?:svg|png|gif|ico))$"));
    QRegularExpressionMatch match = fNameReg.match(firstLine);
    if (!match.hasMatch()) {
        return QString();
    }

    QFileInfo linkInfo(path + QLatin1Char('/') + match.captured(1));
    QString aliasLink = resolveWindowsGitLink(linkInfo.path(), linkInfo.fileName());
    if (!aliasLink.isEmpty()) {
        // qDebug() <<  fileName << "=" << match.captured(1) << "=" << aliasLink;
        return aliasLink;
    }

    return path + QLatin1Char('/') + match.captured(1);
}

/**
 * Generates for the given directories a resource file with the full icon theme.
 * Does some consistency checks, will die if they fail.
 *
 * @param indirs directories that contains the icons of the theme, the first is the versioned stuff,
 *               the remainings contain generated icons
 * @param outfile QRC file to generate
 */
static void generateQRCAndCheckInputs(const QStringList &indirs, const QString &outfile)
{
    QFile out(outfile);
    if (!out.open(QIODevice::WriteOnly)) {
        qFatal() << "Failed to create" << outfile;
    }
    out.write("<!DOCTYPE RCC><RCC version=\"1.0\">\n");
    out.write("<qresource>\n");

    // loop over the inputs, remember if we do look at generated stuff for checks
    bool generatedIcons = false;
    QSet<QString> checkedFiles;
    for (const auto &indir : indirs) {
        // go to input dir to have proper relative paths
        if (!QDir::setCurrent(indir)) {
            qFatal() << "Failed to switch to input directory" << indir;
        }

        // we look at all interesting files in the indir and create a qrc with resolved symlinks
        // we need QDir::System to get broken links for checking
        QDirIterator it(QStringLiteral("."), {QStringLiteral("*.theme"), QStringLiteral("*.svg")}, QDir::Files | QDir::System, QDirIterator::Subdirectories);
        while (it.hasNext()) {
            // ensure nice path without ./ and Co.
            const auto file = QDir::current().relativeFilePath(it.next());
            const QFileInfo fileInfo(file);

            // icons name shall not contain any kind of space
            for (const auto &c : file) {
                if (c.isSpace()) {
                    qFatal() << "Invalid file" << file << "with spaces in the name in input directory" << indir;
                }
            }

            // per default we write the relative name as alias and the full path to pack in
            // allows to generate the resource out of source, will already resolve normal symlinks
            auto fullPath = fileInfo.canonicalFilePath();

            // real symlink resolving for Unices, the rcc compiler ignores such files in -project mode
            bool isLink = false;
            if (fileInfo.isSymLink()) {
                isLink = true;
            }

            // pseudo link files generated by Git on Windows
            else if (const auto aliasLink = resolveWindowsGitLink(fileInfo.path(), fileInfo.fileName()); !aliasLink.isEmpty()) {
                fullPath = QFileInfo(aliasLink).canonicalFilePath();
                isLink = true;
            }

            // more checks for links
            if (isLink) {
                // empty canonical path means not found
                if (fullPath.isEmpty()) {
                    qFatal() << "Broken symlink" << file << "in input directory" << indir;
                }

                // check that we don't link external stuff
                if (!fullPath.startsWith(QFileInfo(indir).canonicalFilePath())) {
                    qFatal() << "Bad symlink" << file << "in input directory" << indir << "to external file" << fullPath;
                }
            }

            // do some checks for SVGs
            // do checks just once, if we encounter this multiple times because of aliasing
            if (fullPath.endsWith(QLatin1String(".svg")) && !checkedFiles.contains(fullPath)) {
                // fill our guard
                checkedFiles.insert(fullPath);

                // validate it as XML if it is an SVG
                validateXml(fullPath);

                // do duplicate check for non-generated icons
                if (!generatedIcons) {
                    checkForDuplicates(fullPath);
                }
            }

            // write the one alias to file entry
            out.write(QStringLiteral("    <file alias=\"%1\">%2</file>\n").arg(file, fullPath).toUtf8());
        }

        // starting with the second directory we look at generated icons
        generatedIcons = true;
    }

    out.write("</qresource>\n");
    out.write("</RCC>\n");
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QCommandLineParser parser;
    QCommandLineOption outOption(QStringList() << QLatin1String("o") << QLatin1String("outfile"), QStringLiteral("Output qrc file"), QStringLiteral("outfile"));
    parser.setApplicationDescription(QLatin1String("Create a resource file from the given input directories handling symlinks and pseudo symlink files."));
    parser.addHelpOption();
    parser.addVersionOption();
    parser.addOption(outOption);
    parser.process(app);

    // do the generation and checks, will die on errors
    generateQRCAndCheckInputs(parser.positionalArguments(), parser.value(outOption));
    return 0;
}
