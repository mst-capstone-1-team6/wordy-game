#!/usr/bin/env bash
set -e
BASEDIR=$(dirname "$0")

rm -rf "$BASEDIR/.downloads/"
mkdir -p "$BASEDIR/.downloads/"
wget -O "$BASEDIR/.downloads/assets_letterTiles_0.zip" https://opengameart.org/sites/default/files/assets_letterTiles_0.zip

unzip "$BASEDIR/.downloads/assets_letterTiles_0.zip" -d "$BASEDIR/.downloads/letterTiles"

rm -rf "$BASEDIR/assets/letter/"
mkdir -p "$BASEDIR/assets/letter/"
mv "$BASEDIR/.downloads/letterTiles/PNG"/* "$BASEDIR/assets/letter/"

