#!/bin/bash

sleep 5
COLOR_VALUES="255 255 255"

echo "$COLOR_VALUES" | sudo tee /sys/class/leds/g15::kbd_backlight/multi_intensity