#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

mathjax="$PREFIX/lib/mathjax"
mkdir -p "$mathjax"

mv config "$mathjax/"
mv docs "$mathjax/"
mv extensions "$mathjax/"
mv fonts "$mathjax/"
mv jax "$mathjax/"
mv localization "$mathjax/"
mv test "$mathjax/"
mv unpacked "$mathjax/"

rm *.md ".gitignore" ".travis.yml" "bower.json" "composer.json" "latest.js" "package.json" || exit 1
cwd="$(pwd)"
cp -r "$cwd/." "$mathjax/"
cd "$mathjax"
rm *.sh LICENSE
cd "$cwd"

mkdir -p "$PREFIX/bin"
cp "${RECIPE_DIR}/mathjax-path" "$PREFIX/bin/"
chmod +x "$PREFIX/bin/mathjax-path"
