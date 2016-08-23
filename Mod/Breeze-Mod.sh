#!/bin/bash
# This script assumes (1) it is run from the directory "/breeze-icons/Mod", (2) the Breeze icon theme will be installed in the directory "~/.icons" and (3) user will refresh or change to Breeze after job completion - otherwise modify the script as needed.
rm -Rf ~/.icons/Breeze
cp -Rf ../icons ~/.icons/Breeze
cp -Rf ../icons-dark/emblems ~/.icons/Breeze
cp -Rf ../icons-dark/status ~/.icons/Breeze
cp -Rf ./Breeze/. ~/.icons/Breeze
cp -f ./index.theme ~/.icons/Breeze/index.theme
gsettings set org.gnome.desktop.interface icon-theme "Breeze"
