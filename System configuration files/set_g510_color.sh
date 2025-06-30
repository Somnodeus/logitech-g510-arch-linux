#!/bin/bash

# Set your desired RGB values ​​here (e.g. for white)
# Format: RED GREEN BLUE (values ​​from 0 to 255, separated by spaces)
COLOR_VALUES="255 255 255" # white

echo "$COLOR_VALUES" > /sys/class/leds/g15::kbd_backlight/multi_intensity