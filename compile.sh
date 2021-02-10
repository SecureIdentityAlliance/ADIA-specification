#!/bin/bash

# So we can see what we're doing
set -x

# Exit with nonzero exit code if anything fails
set -e

# Iterate through the list of Bikeshed files and create the HTML files
for i in *.bs; do
    bikeshed --print=plain spec -f "$i"
done

# Create a fresh directory 'out'
rm -Rf out
mkdir -p out

# Move all the generated HTML files to the output directory

if [ -d out ]; then
    mv *.html out
fi
