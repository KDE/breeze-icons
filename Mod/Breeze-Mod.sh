#!/bin/bash
# This script assumes (1) it is run from the directory "/breeze-icons/Mod", (2) the Breeze icon theme will be installed in the directory "~/.icons" and (3) user will refresh or change to Breeze after job completion - otherwise modify the script as needed.
rm -Rf "$HOME/.icons/Breeze"
cp -Rf "../icons" "$HOME/.icons/Breeze"
cp -Rf "../icons-dark/emblems" "$HOME/.icons/Breeze"
cp -Rf "../icons-dark/status" "$HOME/.icons/Breeze"
cp -Rf "./Breeze/." "$HOME/.icons/Breeze"
cp -f "./index.theme" "$HOME/.icons/Breeze/index.theme"
gtk-update-icon-cache "$HOME/.icons/Breeze" -f
gsettings set org.gnome.desktop.interface icon-theme "Breeze"
