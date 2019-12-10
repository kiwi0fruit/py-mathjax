#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

if [[ "$OSTYPE" == "msys" ]]; then
    mathjax="$(cygpath "${LIBRARY_LIB}")/mathjax"
    bin_dir="$(cygpath "$SCRIPTS")"
else
    mathjax="$PREFIX/lib/mathjax"
    bin_dir="$PREFIX/bin"
fi


for di in ./*
do
    if [[ -d "$di" && ! -d ./mathjax ]]; then
        mv "$di" ./mathjax
    fi
done


mkdir -p "$mathjax"
mv ./mathjax/es5 "$mathjax/"
mv ./mathjax/LICENSE ./


mkdir -p "${bin_dir}"
cp "${RECIPE_DIR}/mathjax-path" "${bin_dir}/"
if [[ "$OSTYPE" == "msys" ]]; then
    cp "${RECIPE_DIR}/mathjax-path.bat" "${bin_dir}/"
else
    chmod +x "${bin_dir}/mathjax-path"
fi
