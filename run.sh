#!/bin/sh

rm -rf www && \
mkdir -p www && \
./main.py src www && \
sass --verbose --no-source-map src/scss/custom.scss www/bootstrap.css  && \
cp -rv assets/* www/

python3 -m http.server -d www
