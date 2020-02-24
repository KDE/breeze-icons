#!/bin/sh

find . -type f -name '*.svg' -exec xmllint --noout {} + 2> xmlerrors
if [ -s xmlerrors ]; then
    cat xmlerrors
    rm xmlerrors
    exit 1
fi
rm xmlerrors
