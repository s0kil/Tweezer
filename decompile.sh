#!/usr/bin/env bash

rm -rf ./decompilations

for file in firmware_binaries/*; do
    ghidrecomp --skip-cache --fa "$file"
done
