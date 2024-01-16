#!/usr/bin/env bash

# Create A Link To Ghidra analyzeHeadless.bat
# ln -s ~/Downloads/ghidra_11.0_PUBLIC/support/analyzeHeadless ~/.local/bin/analyzeHeadless.bat

python3 Tweezer/tweezer.py --model-path firmware_binaries.mdl --binary targets/bmminer_stripped &>targets/bmminer_stripped.log
