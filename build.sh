#!/bin/bash

test -d spacex001 && rm -rf spacex001
mkdir -p spacex001/spacedefense/assets
mkdir -p spacex001/spacedefense/assets/images
mkdir -p spacex001/spacedefense/assets/images

cp -r spacedefense/* spacex001/spacedefense/

cp main.py spacex001/

rm -fr spacex001/spacedefense/__pycache__
rm -fr spacex001/spacedefense/assets/images/vmove_cambg2

python -m pygbag --build spacex001

cp spacex001/build/web/index.html web/index.html
cp spacex001/build/web/spacex001.apk web/spacex001.apk
rm -fr spacex001