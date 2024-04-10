#!/bin/bash

test -d web || mkdir web
test -d spacex001 && rm -rf spacex001
mkdir -p spacex001/spacedefense_wasm/assets/images
mkdir -p spacex001/spacedefense_wasm/assets/sounds

cp -r spacedefense_wasm/* spacex001/spacedefense_wasm/

rm -f spacex001/main.py
cp wasm.py spacex001/main.py

rm -fr spacex001/spacedefense_wasm/__pycache__

python -m pygbag --build spacex001

cp spacex001/build/web/index.html web/index.html
cp spacex001/build/web/spacex001.apk web/spacex001.apk
rm -fr spacex001