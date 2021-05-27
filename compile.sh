#!/bin/bash

# So we can see what we're doing
set -x

# Exit with nonzero exit code if anything fails
set -e

# Remove and create a fresh directory for output distribution
rm -Rf dist
mkdir -p dist


# Iterate through the list of Bikeshed files and create the HTML files
# Execute without installing Bikeshed!!
for i in *.bs; do
    bikeshed --print=plain spec -f "$i"
    # curl https://api.csswg.org/bikeshed/ -F file=@"$i" -F force=1 > "${i%.*}".html
done


# Move all the generated HTML files to the output directory

if [ -d dist ]; then
    mv *.html dist
    cp resources/index.html dist
fi

# Copy static resources - images, sequence diarams and resources to dist

if [ -d resources ]; then
  cp -R resources dist
fi

if [ -d sequence-diagrams ]; then
  cp -R sequence-diagrams dist
fi

if [ -d images ]; then
  cp -R images dist
fi

if [ -d references ]; then
  cp -R references dist
fi
