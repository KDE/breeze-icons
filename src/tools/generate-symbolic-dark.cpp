/* SPDX-FileCopyrightText: 2023 Noah Davis <noahadvs@gmail.com>
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#include <QCommandLineOption>
#include <QCommandLineParser>
#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QDirIterator>
#include <QFile>
#include <QMimeDatabase>
#include <QRegularExpression>
#include <QXmlStreamReader>
#include <QXmlStreamWriter>

using namespace Qt::StringLiterals;
using QRE = QRegularExpression;

// Prevent massive build log files
QString elideString(const QString &string)
{
    static const auto ellipsis = "…"_L1;
    static constexpr auto limit = 100000;
    if (string.size() > limit) {
        return string.first(qBound(0, limit - ellipsis.size(), string.size())) + ellipsis;
    }
    return string;
}

QString convertStylesheet(QString stylesheet)
{
    const auto patternOptions = QRE::MultilineOption | QRE::DotMatchesEverythingOption;
    // Remove whitespace
    stylesheet.remove(QRE(u"\\s"_s, patternOptions));
    // class, color
    QMap<QString, QString> classColorMap;
    // TODO: Support color values other than hexadecimal, maybe properties other than "color"
    QRE regex(u"\\.ColorScheme-(\\S+?){color:(#[0-9a-fA-F]+);}"_s, patternOptions);
    auto matchIt = regex.globalMatch(stylesheet);
    while (matchIt.hasNext()) {
        auto match = matchIt.next();
        auto classString = match.captured(1);
        auto colorString = match.captured(2);
        if (classString == "Text"_L1) {
            colorString = u"#fcfcfc"_s;
        } else if (classString == "Background"_L1) {
            colorString = u"#2a2e32"_s;
        }
        classColorMap.insert(match.captured(1), colorString);
    }

    QString output;
    for (auto it = classColorMap.cbegin(); it != classColorMap.cend(); ++it) {
        output += ".ColorScheme-%1 { color: %2; } "_L1.arg(it.key(), it.value());
    }
    return output;
}

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);

    QCommandLineParser commandLineParser;
    commandLineParser.setApplicationDescription(u"Takes light theme icons and makes modified copies of them with dark theme stylesheets."_s);
    commandLineParser.addPositionalArgument(u"inputs"_s, u"Input folders (separated by spaces)"_s, u"inputs..."_s);
    commandLineParser.addPositionalArgument(u"output"_s, u"Output folder (will be created if not existing)"_s, u"output"_s);
    commandLineParser.addHelpOption();
    commandLineParser.addVersionOption();

    commandLineParser.process(app);

    const auto &positionalArguments = commandLineParser.positionalArguments();
    if (positionalArguments.isEmpty()) {
        qWarning() << "The arguments are missing.";
        return 1;
    }

    QFileInfo outputDirInfo(positionalArguments.last());
    if (outputDirInfo.exists() && !outputDirInfo.isDir()) {
        qWarning() << positionalArguments.last() << "is not a folder.";
        return 1;
    }

    QList<QDir> inputDirs;
    QStringList ignoredArgs;
    for (int i = 0; i < positionalArguments.size() - 1; ++i) {
        QFileInfo inputDirInfo(positionalArguments[i]);
        if (!inputDirInfo.isDir()) {
            ignoredArgs << positionalArguments[i];
            continue;
        }
        inputDirs << inputDirInfo.absoluteFilePath();
    }

    if (inputDirs.isEmpty()) {
        qWarning() << "None of the input arguments could be used.";
        return 1;
    }

    if (!ignoredArgs.isEmpty()) {
        // Using the arg instead of path or filename so the user sees what they typed.
        qWarning() << "The following input arguments were ignored:";
        qWarning().noquote() << elideString(ignoredArgs.join("\n"_L1));
    }

    bool wasAnyFileWritten = false;
    QStringList unreadFiles;
    QStringList unwrittenFiles;
    QStringList xmlReadErrorFiles;
    QStringList xmlWriteErrorFiles;
    for (auto &inputDir : std::as_const(inputDirs)) {
        QDirIterator dirIt(inputDir, QDirIterator::Subdirectories);
        while (dirIt.hasNext()) {
            auto inputFileInfo = dirIt.nextFileInfo();
            const auto inputFilePath = inputFileInfo.absoluteFilePath();

            // Skip non-files, symlinks, non-svgs and existing breeze dark icons
            if (!inputFileInfo.isFile() || inputFileInfo.isSymLink() || !inputFilePath.endsWith(".svg"_L1)
                || QFileInfo::exists(QString{inputFilePath}.replace("/icons/"_L1, "/icons-dark/"_L1))) {
                continue;
            }

            QFile inputFile(inputFilePath);
            if (!inputFile.open(QIODevice::ReadOnly)) {
                unreadFiles.append("\""_L1 + inputFile.fileName() + "\": "_L1 + inputFile.errorString());
                continue;
            }
            const auto inputData = inputFile.readAll();
            inputFile.close();

            // Skip any icons that don't have the stylesheet
            if (!inputData.contains("current-color-scheme")) {
                continue;
            }

            QDir outputDir = outputDirInfo.absoluteFilePath();
            const auto outputFilePath = outputDir.absoluteFilePath(QString{inputFilePath}.remove(QRE(u".*/icons/"_s)));
            QFileInfo outputFileInfo(outputFilePath);
            outputDir = outputFileInfo.dir();
            if (!outputDir.exists()) {
                QDir::root().mkpath(outputDir.absolutePath());
            }
            QFile outputFile(outputFilePath);
            if (!outputFile.open(QIODevice::WriteOnly)) {
                unwrittenFiles.append("\""_L1 + outputFile.fileName() + "\": "_L1 + outputFile.errorString());
                continue;
            }

            QXmlStreamReader reader(inputData);
            reader.setNamespaceProcessing(false);
            QByteArray outputData;
            QXmlStreamWriter writer(&outputData);
            writer.setAutoFormatting(true);

            while (!reader.atEnd() && !reader.hasError() && !writer.hasError()) {
                reader.readNext();
                writer.writeCurrentToken(reader);
                if (!reader.isStartElement() || reader.qualifiedName() != "style"_L1 || reader.attributes().value("id"_L1) != "current-color-scheme"_L1) {
                    continue;
                }
                reader.readNext();
                if (!reader.isCharacters()) {
                    writer.writeCurrentToken(reader);
                    continue;
                }
                writer.writeCharacters(convertStylesheet(reader.text().toString()));
            }

            if (reader.hasError()) {
                xmlReadErrorFiles.append("\""_L1 + inputFile.fileName() + "\": "_L1 + reader.errorString());
            }
            if (writer.hasError()) {
                xmlWriteErrorFiles.append("\""_L1 + outputFile.fileName() + "\""_L1);
            }

            auto bytesWritten = outputFile.write(outputData);
            outputFile.close();
            wasAnyFileWritten |= bytesWritten > 0;
        }
    }

    if (!unreadFiles.empty()) {
        qWarning() << "Input file open errors:";
        qWarning().noquote() << elideString(unreadFiles.join("\n"_L1));
    }
    if (!unwrittenFiles.empty()) {
        qWarning() << "Output file open errors:";
        qWarning().noquote() << elideString(unwrittenFiles.join("\n"_L1));
    }
    if (!xmlReadErrorFiles.empty()) {
        qWarning() << "Input XML read errors:";
        qWarning().noquote() << elideString(xmlReadErrorFiles.join("\n"_L1));
    }
    if (!xmlWriteErrorFiles.empty()) {
        qWarning() << "Output XML write errors:";
        qWarning().noquote() << elideString(xmlWriteErrorFiles.join("\n"_L1));
    }

    return wasAnyFileWritten ? 0 : 1;
}
