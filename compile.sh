#!/bin/bash

# So we can see what we're doing
set -x

# Exit with nonzero exit code if anything fails
set -e

# Iterate through the list of Bikeshed files and create the HTML files
# Execute without installing Bikeshed!!
for i in *.bs; do
    # bikeshed --print=plain spec -f "$i"
    curl https://api.csswg.org/bikeshed/ -F file=@"$i" -F force=1 > "$i".html
done

# Create a fresh directory 'out'
rm -Rf dist
mkdir -p dist

# Move all the generated HTML files to the output directory

if [ -d dist ]; then
    mv *.html dist
fi
