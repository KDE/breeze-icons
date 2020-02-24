#!/bin/bash

set -ex

OUTPUT_DIR=$1

# Compat between freebsd and gnu.
case $(sed --help 2>&1) in
    *GNU*)
        echo "Using GNU-style sed arguments"
        sed_i () {
            sed -i "$@"
        }
        ;;
    *)
        echo "Using POSIX-style sed arguments"
        sed_i () {
            sed -i '' "$@"
        }
        ;;
esac

for INPUT_FILE in {devices,actions,places,status}/22/*.svg; do
    OUTPUT_FILE="$OUTPUT_DIR/${INPUT_FILE/22/24}"
    if [ ! -d $(dirname $OUTPUT_FILE) ] ; then
        mkdir -p $(dirname $OUTPUT_FILE)
    fi

    # It's a symlink to another icon; make a link to mirror the one for the 22px version
    if [ -L $INPUT_FILE ] ; then
        LINK_TARGET=$(readlink $INPUT_FILE)
        ln -fsn $LINK_TARGET $OUTPUT_FILE

    # It's a file; make a 24px version of it
    else
        cp $INPUT_FILE $OUTPUT_FILE

        # Change the size of the bounding box
        if grep --quiet '"0 0 22 22' $OUTPUT_FILE; then
            sed_i -e 's/"0 0 22 22/"0 0 24 24/g' $OUTPUT_FILE
        # YOU
        elif grep --quiet 'width="22"' $OUTPUT_FILE; then
            sed_i -e 's/width="22"/width="24"/g' $OUTPUT_FILE
            sed_i -e 's/height="22"/height="24"/g' $OUTPUT_FILE
        else
            echo $INPUT_FILE does not have the size defined in a parse-able way
            exit 1
        fi

        # Group all the paths and transform them to fit in the center of a 24px box
        if grep --quiet "</defs>" $OUTPUT_FILE; then
            sed_i -e 's|</defs>|</defs><g transform="translate(1,1)">|g' $OUTPUT_FILE
        elif grep --quiet "</style>" $OUTPUT_FILE; then
            sed_i -e 's|</style>|</style><g transform="translate(1,1)">|g' $OUTPUT_FILE
        else
        # No stylesheet or defs tag; put the group at the end of the opening svg tag
            sed_i -e 's|<svg \(.*\)>|<svg \1><g transform="translate(1,1)">|g' $OUTPUT_FILE
        fi

        # Add the closing group tag
        sed_i -e 's|</svg>|</g></svg>|g' $OUTPUT_FILE
    fi
done


# Make the @2x hidpi compatibility dirs
for ICON_DIR in  devices actions places status; do
    ln -fsn 24 $OUTPUT_DIR/$ICON_DIR/24@2x
done
