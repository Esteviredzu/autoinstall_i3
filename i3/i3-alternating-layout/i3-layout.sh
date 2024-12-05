#!/bin/bash

HOME_DIR=$(eval echo ~$USER)
source "$HOME_DIR/.config/i3/i3-alternating-layout/.venv/bin/activate"
python "$HOME_DIR/.config/i3/i3-alternating-layout/alternating_layouts.py"
